"""Modern GUI for the Numbers Discovery Game using ttkbootstrap.

Provides a sleek, light-themed graphical interface for playing the number guessing game.
"""

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledText
from ttkbootstrap.dialogs import Messagebox
from tkinter import simpledialog
from typing import Any, Optional
from game_engine import NumGame, DEFAULT_DIGIT_COUNT
from help_string import get_help_string
from high_scores import add_score, display_leaderboard
from network_manager import NetworkManager, NetworkCallbacks


class NumbersGameGUI(ttk.Frame):
    """Main game window with modern light theme."""
    
    def __init__(self, master: ttk.Window) -> None:
        """Initialize the game GUI."""
        super().__init__(master, padding=15)
        self.master = master
        self.digit_count = DEFAULT_DIGIT_COUNT
        self.game = NumGame(self.digit_count)
        self.tries = 0
        self.hint_penalty = 0
        
        # 2-player mode state
        self.two_player_mode = False
        self.current_player = 1
        self.player1_tries = 0
        self.player2_tries = 0
        self.player1_name = "Player 1"
        self.player2_name = "Player 2"
        self.player1_won = False
        self.player2_won = False
        self.player1_secret = None  # Number set by Player 1 for Player 2 to guess
        self.player2_secret = None  # Number set by Player 2 for Player 1 to guess
        
        # Online mode state
        self.online_mode = False
        self.network: Optional[NetworkManager] = None
        self.is_host = False
        self.opponent_name = "Opponent"
        self.my_online_secret: Optional[int] = None
        self.online_p1_ready = False
        self.online_p2_ready = False
        
        self.pack(fill=BOTH, expand=True)
        self.init_window()

    def init_window(self) -> None:
        """Set up the main window layout."""
        self.master.title("🎮 Numbers Discovery Game")
        self.master.geometry("750x600")
        self.master.minsize(650, 500)
        
        self._create_header()
        self._create_controls()
        self._create_log_area()
        self._create_input_area()
        
        self._log(get_help_string(self.digit_count))
        self._log("\n" + "═" * 50)
        self._log("🎯 Game started! Enter your guess below.")
        self._log("═" * 50 + "\n")

    def _create_header(self) -> None:
        """Create the header with title and stats."""
        header = ttk.Frame(self)
        header.pack(fill=X, pady=(0, 15))
        
        # Title
        title = ttk.Label(
            header, 
            text="🔢 Numbers Discovery",
            font=("Segoe UI", 20, "bold"),
            bootstyle="primary"
        )
        title.pack(side=LEFT, padx=10, pady=5)
        
        # Stats meter
        self.stats_meter = ttk.Meter(
            header,
            metersize=80,
            amountused=100,
            amounttotal=100,
            metertype="semi",
            subtext="Score",
            interactive=False,
            bootstyle="success"
        )
        self.stats_meter.pack(side=RIGHT, padx=10)
        
        # Tries label
        self.tries_label = ttk.Label(
            header,
            text="Tries: 0 | Hints: 0",
            font=("Segoe UI", 11),
            bootstyle="info"
        )
        self.tries_label.pack(side=RIGHT, padx=20)
        
        # Current player indicator (for 2-player mode)
        self.player_label = ttk.Label(
            header,
            text="",
            font=("Segoe UI", 11, "bold"),
            bootstyle="success"
        )
        self.player_label.pack(side=RIGHT, padx=10)

    def _create_controls(self) -> None:
        """Create the control panel with buttons."""
        controls = ttk.Frame(self)
        controls.pack(fill=X, pady=(0, 10))
        
        # Difficulty selector
        diff_frame = ttk.Frame(controls)
        diff_frame.pack(side=LEFT)
        
        ttk.Label(diff_frame, text="Difficulty:", font=("Segoe UI", 10)).pack(side=LEFT, padx=(0, 8))
        self.difficulty_var = ttk.StringVar(value="Medium (5)")
        difficulty_combo = ttk.Combobox(
            diff_frame,
            textvariable=self.difficulty_var,
            values=["Easy (4)", "Medium (5)", "Hard (6)"],
            state="readonly",
            width=12,
            bootstyle="info"
        )
        difficulty_combo.pack(side=LEFT)
        difficulty_combo.bind("<<ComboboxSelected>>", self._on_difficulty_change)
        
        ttk.Label(diff_frame, text="  Mode:", font=("Segoe UI", 10)).pack(side=LEFT, padx=(15, 8))
        self.mode_var = ttk.StringVar(value="1 Player")
        mode_combo = ttk.Combobox(
            diff_frame,
            textvariable=self.mode_var,
            values=["1 Player", "2 Players", "Online"],
            state="readonly",
            width=10,
            bootstyle="success"
        )
        mode_combo.pack(side=LEFT)
        mode_combo.bind("<<ComboboxSelected>>", self._on_mode_change)
        
        # Action buttons
        btn_frame = ttk.Frame(controls)
        btn_frame.pack(side=RIGHT)
        
        ttk.Button(
            btn_frame, text="🎲 New Game", 
            command=self.new_game, 
            bootstyle="success",
            width=12
        ).pack(side=LEFT, padx=3)
        
        ttk.Button(
            btn_frame, text="💡 Hint", 
            command=self.use_hint, 
            bootstyle="warning",
            width=10
        ).pack(side=LEFT, padx=3)
        
        ttk.Button(
            btn_frame, text="📝 Think", 
            command=self.open_thinking_area, 
            bootstyle="info-outline",
            width=10
        ).pack(side=LEFT, padx=3)
        
        ttk.Button(
            btn_frame, text="🏆 Scores", 
            command=self.show_leaderboard, 
            bootstyle="secondary-outline",
            width=10
        ).pack(side=LEFT, padx=3)
        
        ttk.Button(
            btn_frame, text="🏳️ Give Up", 
            command=self.give_up, 
            bootstyle="danger-outline",
            width=12
        ).pack(side=LEFT, padx=3)

    def _create_log_area(self) -> None:
        """Create the scrollable game log(s)."""
        # Container for log areas
        self.log_container = ttk.Frame(self)
        self.log_container.pack(fill=BOTH, expand=True, pady=(0, 10))
        
        # Single player log (default)
        self.single_log_frame = ttk.Labelframe(self.log_container, text="Game Log", bootstyle="info", padding=10)
        self.single_log_frame.pack(fill=BOTH, expand=True)
        
        self.log_area = ScrolledText(
            self.single_log_frame,
            height=12,
            font=("Cascadia Code", 10),
            autohide=True
        )
        self.log_area.pack(fill=BOTH, expand=True)
        
        # Two-player split logs (created but hidden initially)
        self.split_log_frame = ttk.Frame(self.log_container)
        
        # Player 1 log
        self.p1_log_frame = ttk.Labelframe(self.split_log_frame, text="Player 1", bootstyle="success", padding=5)
        self.p1_log_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 5))
        
        self.p1_log_area = ScrolledText(
            self.p1_log_frame,
            height=10,
            font=("Cascadia Code", 9),
            autohide=True
        )
        self.p1_log_area.pack(fill=BOTH, expand=True)
        
        # Player 2 log
        self.p2_log_frame = ttk.Labelframe(self.split_log_frame, text="Player 2", bootstyle="warning", padding=5)
        self.p2_log_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=(5, 0))
        
        self.p2_log_area = ScrolledText(
            self.p2_log_frame,
            height=10,
            font=("Cascadia Code", 9),
            autohide=True
        )
        self.p2_log_area.pack(fill=BOTH, expand=True)

    def _create_input_area(self) -> None:
        """Create the input area."""
        input_frame = ttk.Frame(self)
        input_frame.pack(fill=X, pady=5)
        
        ttk.Label(
            input_frame, 
            text="Your guess:", 
            font=("Segoe UI", 12, "bold")
        ).pack(side=LEFT, padx=(0, 10))
        
        self.input_entry = ttk.Entry(
            input_frame, 
            width=15, 
            font=("Cascadia Code", 14),
            bootstyle="info"
        )
        self.input_entry.pack(side=LEFT, padx=(0, 10))
        self.input_entry.bind("<Return>", self._on_submit)
        self.input_entry.focus()
        
        ttk.Button(
            input_frame, 
            text="Submit ➤", 
            command=self._on_submit,
            bootstyle="success",
            width=12
        ).pack(side=LEFT)

    def _log(self, message: str, player: int = 0) -> None:
        """Add a message to the log area.
        
        Args:
            message: Text to display.
            player: 0 for main/both, 1 for player 1, 2 for player 2.
        """
        if self.two_player_mode and hasattr(self, 'p1_log_area'):
            if player == 0:
                # Log to both players
                self.p1_log_area.insert(END, message + "\n")
                self.p1_log_area.see(END)
                self.p2_log_area.insert(END, message + "\n")
                self.p2_log_area.see(END)
            elif player == 1:
                self.p1_log_area.insert(END, message + "\n")
                self.p1_log_area.see(END)
            elif player == 2:
                self.p2_log_area.insert(END, message + "\n")
                self.p2_log_area.see(END)
        else:
            self.log_area.insert(END, message + "\n")
            self.log_area.see(END)

    def _switch_to_split_view(self) -> None:
        """Switch to split-screen view for 2-player mode."""
        self.single_log_frame.pack_forget()
        self.split_log_frame.pack(fill=BOTH, expand=True)
        
        # Update frame titles with player names
        self.p1_log_frame.config(text=f"🟢 {self.player1_name}")
        self.p2_log_frame.config(text=f"🟠 {self.player2_name}")

    def _switch_to_single_view(self) -> None:
        """Switch back to single log view."""
        self.split_log_frame.pack_forget()
        self.single_log_frame.pack(fill=BOTH, expand=True)

    def _update_stats(self) -> None:
        """Update the stats display."""
        self.tries_label.config(text=f"Tries: {self.tries} | Hints: {self.game.hints_used}")
        # Update score meter
        penalty = self.tries + (self.game.hints_used * 5)
        score = max(0, 100 - penalty)
        self.stats_meter.configure(amountused=score)

    def _on_difficulty_change(self, event=None) -> None:
        """Handle difficulty selection change."""
        difficulty_map = {"Easy (4)": 4, "Medium (5)": 5, "Hard (6)": 6}
        new_digit_count = difficulty_map[self.difficulty_var.get()]
        
        if new_digit_count != self.digit_count:
            self.digit_count = new_digit_count
            self.new_game()

    def _on_mode_change(self, event=None) -> None:
        """Handle game mode change."""
        mode = self.mode_var.get()
        self.two_player_mode = mode == "2 Players"
        self.online_mode = mode == "Online"
        
        # Disconnect existing network if switching away from Online
        if self.network and not self.online_mode:
            self.network.disconnect()
            self.network = None
            
        if self.online_mode:
            self._setup_online_game()
        else:
            self.new_game()

    def _setup_2player_game(self) -> None:
        """Set up a 2-player game with player names and secret numbers."""
        # Get player names
        self._ask_player_names()
        
        # Get secret numbers from each player
        self.player1_secret = self._ask_secret_number(self.player1_name, "for " + self.player2_name + " to guess")
        self.player2_secret = self._ask_secret_number(self.player2_name, "for " + self.player1_name + " to guess")

    # ========================
    # ONLINE MULTIPLAYER
    # ========================
    
    def _setup_online_game(self) -> None:
        """Set up online multiplayer game - show Host/Join dialog."""
        # Reset online state
        self.online_p1_ready = False
        self.online_p2_ready = False
        self.my_online_secret = None
        
        # Initialize network manager with callbacks
        callbacks = NetworkCallbacks(
            on_message=self._on_network_message,
            on_connected=self._on_network_connected,
            on_disconnected=self._on_network_disconnected
        )
        self.network = NetworkManager(callbacks)
        
        # Show Host/Join dialog
        dialog = ttk.Toplevel(self.master)
        dialog.title("🌐 Online Mode")
        dialog.geometry("320x200")
        dialog.transient(self.master)
        dialog.grab_set()
        
        ttk.Label(
            dialog, 
            text="Online Multiplayer",
            font=("Segoe UI", 14, "bold")
        ).pack(pady=15)
        
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=10)
        
        def host():
            dialog.destroy()
            self._host_game()
            
        def join():
            dialog.destroy()
            self._join_game()
            
        def cancel():
            dialog.destroy()
            self.mode_var.set("1 Player")
            self.online_mode = False
            self.new_game()
            
        ttk.Button(
            btn_frame, text="🏠 Host Game",
            command=host, bootstyle="success", width=18
        ).pack(pady=5)
        
        ttk.Button(
            btn_frame, text="🔗 Join Game",
            command=join, bootstyle="info", width=18
        ).pack(pady=5)
        
        ttk.Button(
            dialog, text="Cancel",
            command=cancel, bootstyle="secondary"
        ).pack(pady=10)
        
        dialog.protocol("WM_DELETE_WINDOW", cancel)
        self.master.wait_window(dialog)
        
    def _host_game(self) -> None:
        """Start hosting a game."""
        success, info = self.network.host_game()
        
        if success:
            self.is_host = True
            self._switch_to_single_view()
            self._log(f"🌐 Hosting game on: {info}")
            self._log("⏳ Waiting for opponent to connect...")
            self.master.title(f"Numbers Game - Hosting on {info}")
        else:
            Messagebox.show_error(f"Failed to host: {info}", "Error")
            self.mode_var.set("1 Player")
            self.online_mode = False
            self.new_game()
            
    def _join_game(self) -> None:
        """Join a hosted game."""
        ip = simpledialog.askstring(
            "Join Game",
            "Enter Host IP Address:",
            parent=self.master
        )
        
        if not ip:
            self.mode_var.set("1 Player")
            self.online_mode = False
            self.new_game()
            return
            
        success, info = self.network.join_game(ip.strip())
        
        if success:
            self.is_host = False
            self._switch_to_single_view()
            self._log(f"🌐 Connecting to {ip}...")
        else:
            Messagebox.show_error(f"Connection failed: {info}", "Error")
            self.mode_var.set("1 Player")
            self.online_mode = False
            self.new_game()
            
    def _on_network_connected(self, message: str) -> None:
        """Handle successful network connection (called from network thread)."""
        # Use after() for thread safety
        self.after(0, lambda: self._handle_connected(message))
        
    def _handle_connected(self, message: str) -> None:
        """Process connection on main thread."""
        self._log(f"✅ {message}")
        self.master.title("Numbers Game - Online Connected")
        
        # Get player name
        name = simpledialog.askstring(
            "Your Name",
            "Enter your name:",
            parent=self.master
        ) or "Player"
        
        if self.is_host:
            self.player1_name = name
        else:
            self.player2_name = name
            
        # Send name to opponent
        self.network.send("NAME", name)
        
    def _on_network_disconnected(self, reason: str) -> None:
        """Handle network disconnection (called from network thread)."""
        self.after(0, lambda: self._handle_disconnected(reason))
        
    def _handle_disconnected(self, reason: str) -> None:
        """Process disconnection on main thread."""
        self._log(f"❌ Disconnected: {reason}")
        Messagebox.show_warning(f"Disconnected: {reason}", "Connection Lost")
        
        # Reset to single player
        self.online_mode = False
        self.mode_var.set("1 Player")
        self.network = None
        self.master.title("🎮 Numbers Discovery Game")
        self.new_game()
        
    def _on_network_message(self, msg_type: str, data: Any) -> None:
        """Handle incoming network message (called from network thread)."""
        # Use after() for thread safety - all GUI updates must be on main thread
        self.after(0, lambda: self._handle_network_message(msg_type, data))
        
    def _handle_network_message(self, msg_type: str, data: Any) -> None:
        """Process network message on main thread."""
        if msg_type == "NAME":
            # Opponent sent their name
            self.opponent_name = data
            if self.is_host:
                self.player2_name = data
                self._log(f"👤 Opponent joined: {data}")
                # Host initiates game setup after a short delay
                self.after(500, self._initiate_online_setup)
            else:
                self.player1_name = data
                self._log(f"👤 Host: {data}")
                
        elif msg_type == "SETUP_REQ":
            # Host requesting secret number setup
            self._log("📝 Enter your secret number...")
            self._request_online_secret()
            
        elif msg_type == "SECRET_SET":
            # Opponent has set their secret number
            self._log("🔒 Opponent is ready!")
            if self.is_host:
                self.online_p2_ready = True
                self._check_start_online_game()
                
        elif msg_type == "START":
            # Game is starting
            self._log("\n🎮 Game Started!")
            self._start_online_gameplay()
            
        elif msg_type == "GUESS":
            # Opponent made a guess - check against my secret
            guess = int(data)
            count, place = self._compare_numbers(guess, self.my_online_secret)
            
            # Send result back
            self.network.send("RESULT", {
                "guess": data,
                "count": count,
                "place": place
            })
            
            # Log opponent's guess
            self._log(f"❓ {self.opponent_name} guessed: {data} → {count}/{place}")
            
            # Check if opponent won
            if place == self.digit_count:
                if hasattr(self, 'i_won_online') and self.i_won_online:
                    # I already won - now opponent also won = DRAW
                    self._log(f"\n🤝 IT'S A DRAW!")
                    Messagebox.show_info("Both players cracked the code!", "Draw!")
                else:
                    # Opponent won first - I get one more guess
                    self.opponent_won_online = True
                    self._log(f"\n🎯 {self.opponent_name} cracked your code!")
                    self._log("⏳ You have one final guess for a draw!")
                
        elif msg_type == "RESULT":
            # Received result for my guess
            guess = data["guess"]
            count = data["count"]
            place = data["place"]
            
            # Log my result
            if place == self.digit_count:
                # I won!
                if hasattr(self, 'opponent_won_online') and self.opponent_won_online:
                    # Opponent already won - we both won = DRAW
                    self._log(f"🎉 {guess} → {count}/{place}")
                    self._log(f"\n🤝 IT'S A DRAW!")
                    Messagebox.show_info("Both players cracked the code!", "Draw!")
                else:
                    # I won first - opponent gets one more guess
                    self.i_won_online = True
                    self._log(f"🎉 {guess} → {count}/{place}")
                    self._log(f"\n🎯 You cracked the code!")
                    self._log(f"⏳ Waiting for {self.opponent_name}'s final guess...")
            elif hasattr(self, 'opponent_won_online') and self.opponent_won_online:
                # I missed my final chance - opponent wins
                self._log(f"⚫ {guess} → {count}/{place}")
                self._log(f"\n🏆 {self.opponent_name} wins!")
                Messagebox.show_info(f"{self.opponent_name} cracked your code!", "Game Over")
            elif place > 0:
                self._log(f"🟡 {guess} → {count}/{place}")
            elif count > 0:
                self._log(f"🟠 {guess} → {count}/{place}")
            else:
                self._log(f"⚫ {guess} → {count}/{place}")
                
    def _initiate_online_setup(self) -> None:
        """Host sends setup request to both players."""
        self.network.send("SETUP_REQ", self.digit_count)
        self._log("📝 Enter your secret number...")
        self._request_online_secret()
        
    def _request_online_secret(self) -> None:
        """Ask user to enter their secret number for online play."""
        my_name = self.player1_name if self.is_host else self.player2_name
        num = self._ask_secret_number(my_name, "for opponent to guess")
        self.my_online_secret = num
        
        # Notify opponent that I'm ready
        self.network.send("SECRET_SET", True)
        self._log("✅ Secret number set! Waiting for opponent...")
        
        if self.is_host:
            self.online_p1_ready = True
            self._check_start_online_game()
            
    def _check_start_online_game(self) -> None:
        """Host checks if both players are ready to start."""
        if self.is_host and self.online_p1_ready and self.online_p2_ready:
            self.after(500, self._start_online_game)
            
    def _start_online_game(self) -> None:
        """Host starts the online game."""
        self.network.send("START", self.digit_count)
        self._start_online_gameplay()
        
    def _start_online_gameplay(self) -> None:
        """Initialize gameplay phase for online mode."""
        self.current_player = 1
        self.tries = 0
        # Reset win tracking for fair play
        self.i_won_online = False
        self.opponent_won_online = False
        self._log(f"\n🎯 Guess your opponent's {self.digit_count}-digit number!")
        self._log("Enter your guess below.\n")

    def _ask_player_names(self) -> None:
        """Ask for player names in 2-player mode."""
        dialog = ttk.Toplevel(self.master)
        dialog.title("👥 2-Player Mode")
        dialog.geometry("350x200")
        dialog.transient(self.master)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Enter player names:", font=("Segoe UI", 12, "bold")).pack(pady=10)
        
        frame1 = ttk.Frame(dialog)
        frame1.pack(pady=5)
        ttk.Label(frame1, text="Player 1:", width=10).pack(side=LEFT)
        p1_entry = ttk.Entry(frame1, width=20)
        p1_entry.insert(0, self.player1_name)
        p1_entry.pack(side=LEFT)
        
        frame2 = ttk.Frame(dialog)
        frame2.pack(pady=5)
        ttk.Label(frame2, text="Player 2:", width=10).pack(side=LEFT)
        p2_entry = ttk.Entry(frame2, width=20)
        p2_entry.insert(0, self.player2_name)
        p2_entry.pack(side=LEFT)
        
        def submit():
            self.player1_name = p1_entry.get().strip() or "Player 1"
            self.player2_name = p2_entry.get().strip() or "Player 2"
            dialog.destroy()
        
        ttk.Button(dialog, text="Next", command=submit, bootstyle="success").pack(pady=15)
        p1_entry.focus()
        self.master.wait_window(dialog)

    def _ask_secret_number(self, player_name: str, description: str) -> int:
        """Ask a player to enter their secret number."""
        dialog = ttk.Toplevel(self.master)
        dialog.title(f"🔐 {player_name}'s Secret Number")
        dialog.geometry("400x200")
        dialog.transient(self.master)
        dialog.grab_set()
        
        ttk.Label(
            dialog, 
            text=f"{player_name}, enter your secret {self.digit_count}-digit number\n{description}:",
            font=("Segoe UI", 11),
            justify="center"
        ).pack(pady=15)
        
        ttk.Label(
            dialog,
            text="(Other player, look away!)",
            font=("Segoe UI", 9, "italic"),
            bootstyle="warning"
        ).pack()
        
        num_entry = ttk.Entry(dialog, width=15, font=("Cascadia Code", 14), show="*")
        num_entry.pack(pady=10)
        num_entry.focus()
        
        result = [None]
        error_label = ttk.Label(dialog, text="", bootstyle="danger")
        error_label.pack()
        
        def submit():
            num_str = num_entry.get().strip()
            # Validate using game engine
            temp_game = NumGame(self.digit_count)
            is_valid, error_msg = temp_game.check_input(num_str)
            if is_valid:
                result[0] = int(num_str)
                dialog.destroy()
            else:
                error_label.config(text=f"❌ {error_msg}")
                num_entry.delete(0, END)
        
        num_entry.bind("<Return>", lambda e: submit())
        ttk.Button(dialog, text="Confirm", command=submit, bootstyle="success").pack(pady=10)
        
        self.master.wait_window(dialog)
        return result[0]

    def _on_submit(self, event=None) -> None:
        """Handle guess submission."""
        guess = self.input_entry.get().strip()
        self.input_entry.delete(0, END)
        
        if not guess:
            return
        
        is_valid, processed_val, error_msg = self.game.get_input(guess)
        
        if not is_valid:
            self._log(f"❌ {error_msg}")
            return
        
        if processed_val == 'e':
            self.give_up()
            return
        
        # Handle Online mode - send guess to opponent
        if self.online_mode and self.network and self.network.connected:
            self.network.send("GUESS", str(processed_val))
            self._log(f"📤 You guessed: {processed_val}")
            self.tries += 1
            return
        
        # Handle 2-player mode with player-set numbers
        if self.two_player_mode:
            if self.current_player == 1:
                self.player1_tries += 1
                player_name = self.player1_name
                target_number = self.player2_secret  # P1 guesses P2's secret
                opponent_name = self.player2_name
            else:
                self.player2_tries += 1
                player_name = self.player2_name
                target_number = self.player1_secret  # P2 guesses P1's secret
                opponent_name = self.player1_name
            
            # Compare against opponent's secret number
            count, place = self._compare_numbers(processed_val, target_number)
            tries_count = self.player1_tries if self.current_player == 1 else self.player2_tries
            
            # Color-coded feedback
            if place == self.digit_count:
                emoji = "🎉"
            elif place > 0:
                emoji = "🟡"
            elif count > 0:
                emoji = "🟠"
            else:
                emoji = "⚫"
            
            self._log(f"{emoji} #{tries_count}) {guess} → {count}/{place}", player=self.current_player)
            self._update_stats()
            
            if count == place == self.digit_count:
                # Player guessed correctly!
                if self.current_player == 1:
                    # P1 wins - but P2 gets one more chance for a draw
                    self.player1_won = True
                    self._log(f"\n🎯 {self.player1_name} cracked the code!", player=1)
                    self._log(f"\n🎯 {self.player1_name} cracked the code!", player=2)
                    self._log(f"⏳ {self.player2_name} gets one final guess...", player=1)
                    self._log(f"⏳ {self.player2_name} gets one final guess for a draw!", player=2)
                    self.current_player = 2
                    self._update_player_indicator()
                else:
                    # P2 guessed correctly
                    self.player2_won = True
                    if self.player1_won:
                        # Both won with same tries - DRAW!
                        self._handle_draw()
                    else:
                        # P2 wins outright
                        self._handle_win()
            else:
                # Incorrect guess
                if self.current_player == 2 and self.player1_won:
                    # P2 failed their final guess - P1 wins
                    self._handle_win(winner=1)
                else:
                    # Switch players
                    self.current_player = 2 if self.current_player == 1 else 1
                    self._update_player_indicator()
        else:
            # Single player mode
            self.tries += 1
            count, place = self.game.compare(processed_val)
            
            if place == self.digit_count:
                emoji = "🎉"
            elif place > 0:
                emoji = "🟡"
            elif count > 0:
                emoji = "🟠"
            else:
                emoji = "⚫"
            
            self._log(f"{emoji} {self.tries}) {guess} → {count}/{place}")
            self._update_stats()
            
            if count == place == self.digit_count:
                self._handle_win()

    def _compare_numbers(self, guess: int, target: int) -> tuple:
        """Compare a guess against a target number."""
        ref_n = str(target)
        ip_s = str(guess)
        count = 0
        place = 0
        
        for i in range(len(ref_n)):
            val_i = ref_n[i]
            for j in range(len(ip_s)):
                val_j = ip_s[j]
                if val_i == val_j:
                    count += 1
                    if i == j:
                        place += 1
        return count, place

    def _handle_win(self, winner: int = None) -> None:
        """Handle winning the game."""
        if self.two_player_mode:
            # Determine winner
            if winner is None:
                winner = self.current_player
                
            winner_name = self.player1_name if winner == 1 else self.player2_name
            loser_name = self.player2_name if winner == 1 else self.player1_name
            winner_tries = self.player1_tries if winner == 1 else self.player2_tries
            cracked_number = self.player2_secret if winner == 1 else self.player1_secret
            score = max(1, 100 - winner_tries + 1)
            
            self._log(f"\n🎊 {winner_name} WINS!", player=1)
            self._log(f"🔓 Cracked: {cracked_number}", player=1)
            self._log(f"⭐ Tries: {winner_tries}\n", player=1)
            
            self._log(f"\n🎊 {winner_name} WINS!", player=2)
            self._log(f"🔓 Cracked: {cracked_number}", player=2)
            self._log(f"⭐ Tries: {winner_tries}\n", player=2)
            
            if Messagebox.yesno(f"{winner_name} cracked {loser_name}'s number!\n\nScore: {score}\n\nPlay again?", "🎉 Game Over!"):
                self.new_game()
        else:
            score = max(1, 100 - self.tries + 1 - (self.game.hints_used * 5))
            
            self._log("\n" + "🎊 " + "═" * 45)
            self._log(f"   🏆 YOU WON! The number was {self.game.num}")
            self._log(f"   ⭐ Score: {score}/100 (Tries: {self.tries}, Hints: {self.game.hints_used})")
            self._log("═" * 49 + "\n")
            
            name = self._ask_player_name()
            if name:
                rank = add_score(name, self.tries, self.game.hints_used, score, self.digit_count)
                self._log(f"🏅 {name} ranked #{rank} on the leaderboard!\n")
            
            if Messagebox.yesno(f"You won with score {score}!\n\nPlay again?", "🎉 Congratulations!"):
                self.new_game()

    def _handle_draw(self) -> None:
        """Handle a draw when both players crack the code on the same turn."""
        self._log(f"\n🤝 IT'S A DRAW!", player=1)
        self._log(f"Both players cracked the code in {self.player1_tries} tries!", player=1)
        
        self._log(f"\n🤝 IT'S A DRAW!", player=2)
        self._log(f"Both players cracked the code in {self.player2_tries} tries!", player=2)
        
        if Messagebox.yesno("It's a draw! Both players cracked the code!\n\nPlay again?", "🤝 Draw!"):
            self.new_game()

    def _update_player_indicator(self) -> None:
        """Update the current player indicator."""
        if self.two_player_mode:
            current_name = self.player1_name if self.current_player == 1 else self.player2_name
            style = "success" if self.current_player == 1 else "warning"
            self.player_label.config(text=f"🎮 {current_name}'s turn", bootstyle=style)
        else:
            self.player_label.config(text="")

    def _ask_player_name(self) -> str:
        """Ask player for their name."""
        dialog = ttk.Toplevel(self.master)
        dialog.title("🏆 High Score!")
        dialog.geometry("350x150")
        dialog.transient(self.master)
        dialog.grab_set()
        
        ttk.Label(
            dialog, 
            text="Enter your name for the leaderboard:",
            font=("Segoe UI", 11)
        ).pack(pady=15)
        
        name_entry = ttk.Entry(dialog, width=25, font=("Segoe UI", 12))
        name_entry.pack(pady=5)
        name_entry.focus()
        
        result = [None]
        
        def submit():
            result[0] = name_entry.get().strip() or "Anonymous"
            dialog.destroy()
        
        name_entry.bind("<Return>", lambda e: submit())
        ttk.Button(
            dialog, 
            text="Save Score", 
            command=submit,
            bootstyle="success"
        ).pack(pady=15)
        
        self.master.wait_window(dialog)
        return result[0]

    def new_game(self) -> None:
        """Start a new game."""
        self.game = NumGame(self.digit_count)
        self.tries = 0
        self.hint_penalty = 0
        
        # Reset 2-player state
        self.current_player = 1
        self.player1_tries = 0
        self.player2_tries = 0
        self.player1_won = False
        self.player2_won = False
        self.player1_secret = None
        self.player2_secret = None
        
        # Clear logs
        self.log_area.delete(1.0, END)
        if hasattr(self, 'p1_log_area'):
            self.p1_log_area.delete(1.0, END)
            self.p2_log_area.delete(1.0, END)
        
        if self.two_player_mode:
            # Set up 2-player game with secret numbers
            self._setup_2player_game()
            
            # Switch to split view
            self._switch_to_split_view()
            
            self._log(f"🎮 vs {self.player2_name}'s number", player=1)
            self._log(f"Crack their code to win!\n", player=1)
            self._log(f"🎮 vs {self.player1_name}'s number", player=2)
            self._log(f"Crack their code to win!\n", player=2)
            self._update_player_indicator()
        else:
            # Switch to single view
            self._switch_to_single_view()
            self._log(f"🎮 New {self.digit_count}-digit game started!")
            self._log("Enter your guess below.\n")
            self.player_label.config(text="")
        
        self._update_stats()
        self.stats_meter.configure(amountused=100)
        self.input_entry.focus()

    def use_hint(self) -> None:
        """Reveal a hint to the player."""
        position, digit = self.game.get_hint()
        self._log(f"💡 Hint: Position {position + 1} is '{digit}'")
        self._update_stats()

    def give_up(self) -> None:
        """Reveal the answer and offer new game."""
        self._log(f"\n😔 The answer was: {self.game.num}")
        if Messagebox.yesno(f"The number was {self.game.num}\n\nPlay again?", "Game Over"):
            self.new_game()

    def show_leaderboard(self) -> None:
        """Display the leaderboard."""
        self._log(display_leaderboard(self.digit_count))

    def open_thinking_area(self) -> None:
        """Open the thinking area window."""
        ThinkingAreaWindow(self.master, self.digit_count)


class ThinkingAreaWindow(ttk.Toplevel):
    """A modern helper window for tracking guesses."""
    
    def __init__(self, master: ttk.Window, digit_count: int = 5) -> None:
        """Initialize the thinking area window."""
        super().__init__(master)
        self.digit_count = digit_count
        self.title("📝 Thinking Area")
        self.geometry("550x600")
        self.init_ui()
    
    def init_ui(self) -> None:
        """Set up the thinking area UI."""
        # Instructions
        ttk.Label(
            self, 
            text="Track your guesses: Enter numbers and mark T (correct) or F (wrong)",
            font=("Segoe UI", 10),
            bootstyle="dark"
        ).pack(pady=10)
        
        # Matrix frame
        matrix_frame = ttk.Labelframe(self, text="Guess Tracking", bootstyle="info", padding=10)
        matrix_frame.pack(padx=15, pady=10, fill=BOTH, expand=True)
        
        # Headers
        ttk.Label(matrix_frame, text="Number", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, padx=8, pady=5)
        for col in range(self.digit_count):
            ttk.Label(
                matrix_frame, 
                text=f"Pos {col+1}",
                font=("Segoe UI", 9)
            ).grid(row=0, column=col+1, padx=5, pady=5)
        
        self.number_entries = []
        self.matrix_vars = []
        
        for row in range(self.digit_count):
            entry = ttk.Entry(matrix_frame, width=10, font=("Cascadia Code", 10))
            entry.grid(row=row+1, column=0, padx=8, pady=4)
            self.number_entries.append(entry)
            
            row_vars = []
            for col in range(self.digit_count):
                var = ttk.StringVar(value="")
                combo = ttk.Combobox(
                    matrix_frame, 
                    textvariable=var,
                    values=["", "T", "F"],
                    state="readonly",
                    width=4,
                    bootstyle="dark"
                )
                combo.grid(row=row+1, column=col+1, padx=3, pady=4)
                row_vars.append(var)
            self.matrix_vars.append(row_vars)
        
        # Digit availability (which digits could be in the answer)
        avail_frame = ttk.Labelframe(self, text="Digit Availability", bootstyle="secondary", padding=10)
        avail_frame.pack(padx=15, pady=5, fill=X)
        
        self.digit_avail_vars = []
        for i in range(10):
            frame = ttk.Frame(avail_frame)
            frame.pack(side=LEFT, padx=5)
            ttk.Label(frame, text=str(i), font=("Segoe UI", 9, "bold")).pack()
            var = ttk.StringVar(value="")
            combo = ttk.Combobox(
                frame, 
                textvariable=var,
                values=["", "T", "F"],
                state="readonly",
                width=3
            )
            combo.pack()
            self.digit_avail_vars.append(var)
        
        # Digit used (which digits have been confirmed in the answer)
        used_frame = ttk.Labelframe(self, text="Digit Used", bootstyle="info", padding=10)
        used_frame.pack(padx=15, pady=5, fill=X)
        
        self.digit_used_checkboxes = []
        for i in range(10):
            var = ttk.BooleanVar(value=False)
            cb = ttk.Checkbutton(
                used_frame, 
                text=str(i), 
                variable=var,
                bootstyle="warning-round-toggle"
            )
            cb.pack(side=LEFT, padx=8)
            self.digit_used_checkboxes.append(var)
        
        ttk.Button(
            self, 
            text="🗑️ Clear All", 
            command=self.clear_all,
            bootstyle="danger-outline"
        ).pack(pady=15)
    
    def clear_all(self) -> None:
        """Reset all tracking data."""
        for entry in self.number_entries:
            entry.delete(0, END)
        for row_vars in self.matrix_vars:
            for var in row_vars:
                var.set("")
        for var in self.digit_avail_vars:
            var.set("")
        for cb_var in self.digit_used_checkboxes:
            cb_var.set(False)


def main() -> None:
    """Run the GUI application."""
    app = ttk.Window(
        title="Numbers Discovery Game",
        themename="flatly",  # Modern light theme
        size=(750, 600)
    )
    NumbersGameGUI(app)
    app.mainloop()


if __name__ == "__main__":
    main()
