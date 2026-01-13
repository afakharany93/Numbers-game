"""Help string module for the Numbers Game.

Contains the game instructions and rules displayed to players.
"""

from typing import Optional


def get_help_string(digit_count: int = 5) -> str:
    """Generate the help/instructions string for the game.
    
    Args:
        digit_count: Number of digits in the game (for dynamic help text).
        
    Returns:
        Formatted help string with game rules and instructions.
    """
    return f"""Number Discovery Game
*****************
This game is made by: Ahmed Essam El Fakharany
afakharany93@gmail.com
*****************

The Rules:
The computer will generate a random {digit_count} digit number.
Your mission is to guess the number in the least amount of tries.

Each try you'll input a {digit_count} digit number as a guess. The computer will compare
your guess to the number and give you an answer in the form of (Number1/Number2).

- Number1: The amount of digits from your guess that exist in the secret number.
- Number2: The amount of digits that are also in the correct position.

Example:
The computer generates a random number: 28461
Your initial guess is: 26798
The computer will reply 3/1
- The 3 means that 2, 6, and 8 exist in the secret number.
- The 1 means that the 2 is in the correct position.

Rules for the generated number:
1. The number may never start with a 0.
2. A single digit may never repeat in the number.

Invalid examples:
- 02314: Can't start with 0.
- 22314: Can't have the same digit twice.

Commands:
- Type 'e' to reveal the answer and quit.
- Type 'h' to get a hint (costs points).
- Type 'r' to restart the game.

*********************************************
"""


# Keep backward compatibility
help_string = get_help_string(5)
