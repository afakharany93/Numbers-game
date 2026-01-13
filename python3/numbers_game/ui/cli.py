"""Command-line interface for the Numbers Game.

A number guessing game where players try to guess a randomly generated number
with no duplicate digits and not starting with zero.
"""

from numbers_game.core import GameEngine, DEFAULT_DIGIT_COUNT
from numbers_game.utils import get_help_string


def select_difficulty() -> int:
    """Let the player choose the difficulty level.
    
    Returns:
        Number of digits for the game (4, 5, or 6).
    """
    print("\nSelect difficulty:")
    print("  1. Easy (4 digits)")
    print("  2. Medium (5 digits)")
    print("  3. Hard (6 digits)")
    
    while True:
        choice = input("Enter choice (1-3) or press Enter for Medium: ").strip()
        if choice == '' or choice == '2':
            return 5
        elif choice == '1':
            return 4
        elif choice == '3':
            return 6
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


def play_game() -> None:
    """Main game loop."""
    play_again = True
    
    while play_again:
        print("*" * 79)
        play_again = False
        
        # Select difficulty
        digit_count = select_difficulty()
        
        # Show help
        print(get_help_string(digit_count))
        input("Press Enter to start\n")
        
        # Initialize game
        game = GameEngine(digit_count)
        solved = False
        tries = 0
        hint_penalty = 0
        
        while not solved:
            x = input('Enter number: ').strip().lower()
            
            # Handle special commands
            if x == 'e':
                print(f'The solution was {game.num}')
                print('Quit game')
                break
            elif x == 'h':
                position, digit = game.get_hint()
                print(f'Hint: Position {position + 1} is "{digit}"')
                hint_penalty += 5
                continue
            elif x == 'r':
                print('Restarting game...')
                game = GameEngine(digit_count)
                tries = 0
                hint_penalty = 0
                continue
            
            # Validate and process guess
            flag, processed_x, mesg_string = game.get_input(x)
            
            if flag and processed_x is not None:
                tries += 1
                count, place = game.compare(processed_x)
                print(f'{tries}) Reply for {processed_x} is {count}/{place}')
                
                if count == place == digit_count:
                    print('You won!')
                    base_score = max(1, 100 - tries + 1 - hint_penalty)
                    print(f'Your score is {base_score}/100')
                    solved = True
                    
                    y = input('Play again?\n  Type "y" for yes\n  Press any other key to exit\n')
                    if y.lower() == 'y':
                        play_again = True
            else:
                print(mesg_string)


def main() -> None:
    """Entry point for CLI."""
    play_game()


if __name__ == '__main__':
    main()
