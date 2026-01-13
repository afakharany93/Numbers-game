"""Thinking Area Window - A helper window for tracking guesses.

Provides a grid-based interface for tracking guess digits and their positions.
"""

import ttkbootstrap as ttk
from ttkbootstrap.constants import END, BOTH, LEFT, X


class ThinkingAreaWindow(ttk.Toplevel):
    """A modern helper window for tracking guesses."""
    
    def __init__(self, master: ttk.Window, digit_count: int = 5) -> None:
        """Initialize the thinking area window.
        
        Args:
            master: Parent window.
            digit_count: Number of digits in the game.
        """
        super().__init__(master)
        self.digit_count = digit_count
        self.title("📝 Thinking Area")
        self.geometry("550x600")
        self._init_ui()
    
    def _init_ui(self) -> None:
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
