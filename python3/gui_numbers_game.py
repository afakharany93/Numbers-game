"""Modern GUI for the Numbers Discovery Game using ttkbootstrap.

Provides a sleek, light-themed graphical interface for playing the number guessing game.
"""

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledText  # noqa: F401
from ttkbootstrap.dialogs import Messagebox
from game_engine import NumGame, DEFAULT_DIGIT_COUNT
from help_string import get_help_string
from high_scores import add_score, display_leaderboard


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
        """Create the scrollable game log."""
        log_frame = ttk.Labelframe(self, text="Game Log", bootstyle="info", padding=10)
        log_frame.pack(fill=BOTH, expand=True, pady=(0, 10))
        
        self.log_area = ScrolledText(
            log_frame,
            height=12,
            font=("Cascadia Code", 10),
            autohide=True
        )
        self.log_area.pack(fill=BOTH, expand=True)

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

    def _log(self, message: str) -> None:
        """Add a message to the log area."""
        self.log_area.insert(END, message + "\n")
        self.log_area.see(END)

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
        
        self.tries += 1
        count, place = self.game.compare(processed_val)
        
        # Color-coded feedback
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

    def _handle_win(self) -> None:
        """Handle winning the game."""
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
        
        self.log_area.delete(1.0, END)
        self._log(f"🎮 New {self.digit_count}-digit game started!")
        self._log("Enter your guess below.\n")
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
