"""Network manager for online multiplayer functionality.

Handles socket connections, message passing, and threading for non-blocking I/O.
Uses a Host/Client model where one player hosts and the other joins via IP.
"""

import socket
import threading
import json
from typing import Callable, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum


class MessageType(Enum):
    """Types of network messages."""
    NAME = "NAME"
    SETUP_REQ = "SETUP_REQ"
    SECRET_SET = "SECRET_SET"
    START = "START"
    GUESS = "GUESS"
    RESULT = "RESULT"
    DISCONNECT = "DISCONNECT"


@dataclass
class NetworkCallbacks:
    """Callbacks for network events."""
    on_message: Callable[[str, Any], None]
    on_connected: Callable[[str], None]
    on_disconnected: Callable[[str], None]


class NetworkManager:
    """Handles network connections for online multiplayer.
    
    Supports both hosting and joining games over TCP sockets.
    All callbacks are invoked from background threads - GUI code must
    use thread-safe mechanisms (e.g., tkinter's after()) to update UI.
    """
    
    DEFAULT_PORT = 5555
    MSG_SEPARATOR = "|||"
    BUFFER_SIZE = 4096
    
    def __init__(self, callbacks: NetworkCallbacks) -> None:
        """Initialize the network manager.
        
        Args:
            callbacks: NetworkCallbacks with on_message, on_connected, on_disconnected
        """
        self.callbacks = callbacks
        self.sock: Optional[socket.socket] = None
        self.server_sock: Optional[socket.socket] = None
        self.is_host = False
        self.connected = False
        self.running = False
        self._recv_thread: Optional[threading.Thread] = None
        self._accept_thread: Optional[threading.Thread] = None
        
    def host_game(self, port: int = DEFAULT_PORT) -> Tuple[bool, str]:
        """Start hosting a game server.
        
        Args:
            port: Port to listen on
            
        Returns:
            Tuple of (success, message/IP)
        """
        try:
            self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_sock.bind(('', port))
            self.server_sock.listen(1)
            self.server_sock.settimeout(0.5)  # Non-blocking accept
            
            self.running = True
            self.is_host = True
            
            # Start accept thread
            self._accept_thread = threading.Thread(
                target=self._accept_loop,
                daemon=True
            )
            self._accept_thread.start()
            
            # Get local IP for display
            local_ip = self._get_local_ip()
            return True, local_ip
            
        except OSError as e:
            return False, f"Failed to start server: {e}"
            
    def join_game(self, host_ip: str, port: int = DEFAULT_PORT) -> Tuple[bool, str]:
        """Join a hosted game.
        
        Args:
            host_ip: IP address of the host
            port: Port to connect to
            
        Returns:
            Tuple of (success, message)
        """
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(10.0)  # Connection timeout
            self.sock.connect((host_ip, port))
            self.sock.settimeout(None)  # Switch to blocking for recv
            
            self.connected = True
            self.running = True
            self.is_host = False
            
            # Notify connection
            self.callbacks.on_connected("Connected to host")
            
            # Start receive thread
            self._start_receive_thread()
            
            return True, "Connected successfully"
            
        except socket.timeout:
            return False, "Connection timed out"
        except ConnectionRefusedError:
            return False, "Connection refused - is the host running?"
        except OSError as e:
            return False, f"Connection failed: {e}"
            
    def send(self, msg_type: str, data: Any = None) -> bool:
        """Send a message to the other player.
        
        Args:
            msg_type: Type of message (from MessageType enum)
            data: Optional data payload
            
        Returns:
            True if sent successfully
        """
        if not self.connected or not self.sock:
            return False
            
        try:
            packet = json.dumps({
                'type': msg_type,
                'data': data
            }) + self.MSG_SEPARATOR
            self.sock.sendall(packet.encode('utf-8'))
            return True
        except OSError as e:
            print(f"Send error: {e}")
            self._handle_disconnect("Send failed")
            return False
            
    def disconnect(self) -> None:
        """Close connection and cleanup."""
        was_connected = self.connected
        self.connected = False
        self.running = False
        
        # Close client socket
        if self.sock:
            try:
                self.sock.close()
            except OSError:
                pass
            self.sock = None
            
        # Close server socket
        if self.server_sock:
            try:
                self.server_sock.close()
            except OSError:
                pass
            self.server_sock = None
            
        if was_connected:
            self.callbacks.on_disconnected("Connection closed")
            
    def _get_local_ip(self) -> str:
        """Get the local IP address for LAN connections."""
        try:
            # Connect to an external address to determine local IP
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect(("8.8.8.8", 80))
                return s.getsockname()[0]
        except OSError:
            return socket.gethostbyname(socket.gethostname())
            
    def _accept_loop(self) -> None:
        """Accept incoming connection (host only)."""
        while self.running and not self.connected:
            try:
                conn, addr = self.server_sock.accept()
                self.sock = conn
                self.connected = True
                
                # Close server socket - only one connection needed
                if self.server_sock:
                    self.server_sock.close()
                    self.server_sock = None
                    
                self.callbacks.on_connected(f"Player joined from {addr[0]}")
                
                # Start receive thread
                self._start_receive_thread()
                break
                
            except socket.timeout:
                continue
            except OSError:
                break
                
    def _start_receive_thread(self) -> None:
        """Start the receive thread."""
        self._recv_thread = threading.Thread(
            target=self._receive_loop,
            daemon=True
        )
        self._recv_thread.start()
        
    def _receive_loop(self) -> None:
        """Receive and process incoming messages."""
        buffer = ""
        
        while self.running and self.connected and self.sock:
            try:
                data = self.sock.recv(self.BUFFER_SIZE)
                if not data:
                    # Connection closed by peer
                    break
                    
                buffer += data.decode('utf-8')
                
                # Process complete messages
                while self.MSG_SEPARATOR in buffer:
                    msg_str, buffer = buffer.split(self.MSG_SEPARATOR, 1)
                    if msg_str:
                        self._process_message(msg_str)
                        
            except socket.timeout:
                continue
            except OSError:
                break
                
        # Connection ended
        self._handle_disconnect("Connection lost")
        
    def _process_message(self, msg_str: str) -> None:
        """Parse and dispatch a received message."""
        try:
            msg = json.loads(msg_str)
            msg_type = msg.get('type', '')
            data = msg.get('data')
            self.callbacks.on_message(msg_type, data)
        except json.JSONDecodeError:
            print(f"Invalid message received: {msg_str[:50]}")
            
    def _handle_disconnect(self, reason: str) -> None:
        """Handle disconnection cleanup."""
        if self.connected:
            self.connected = False
            self.running = False
            self.callbacks.on_disconnected(reason)
