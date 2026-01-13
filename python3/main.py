#!/usr/bin/env python3
"""Main entry point for the Numbers Discovery Game.

Run this file to start the graphical user interface.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import ttkbootstrap as ttk

# Import the main game GUI
# For now, continue using the existing gui_numbers_game module
# until all imports are updated
from gui_numbers_game import NumbersGameGUI


def main() -> None:
    """Launch the Numbers Discovery Game GUI."""
    app = ttk.Window(
        title="Numbers Discovery Game",
        themename="flatly",  # Modern light theme
        size=(750, 600)
    )
    NumbersGameGUI(app)
    app.mainloop()


if __name__ == "__main__":
    main()
