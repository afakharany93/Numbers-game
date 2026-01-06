"""Number Discovery Game Engine.

This module contains the core game logic for the Numbers Game,
a number guessing game where players try to guess a randomly generated number.
"""

import random
from typing import Tuple, Optional, Union

# Configurable game settings
DEFAULT_DIGIT_COUNT = 5


class NumGame:
    """Main game class that handles number generation, validation, and comparison.
    
    Attributes:
        digit_count: Number of digits in the secret number (default: 5).
        num: The randomly generated secret number to guess.
        hints_used: Number of hints the player has used.
    """
    
    def __init__(self, digit_count: int = DEFAULT_DIGIT_COUNT) -> None:
        """Initialize a new game with a randomly generated number.
        
        Args:
            digit_count: Number of digits for the secret number (4-6).
        """
        self.digit_count = digit_count
        self.num = self.generate_number()
        self.hints_used = 0

    def check_input(self, ip: str) -> Tuple[bool, Optional[str]]:
        """Validate user input against game rules.
        
        Args:
            ip: The user's input string to validate.
            
        Returns:
            A tuple of (is_valid, error_message). If valid, error_message is None.
        """
        mesg_string: Optional[str] = None
        
        # Check if the input has correct length
        if len(ip) != self.digit_count:
            mesg_string = f'Length of input number is not {self.digit_count} digits'
            return False, mesg_string
            
        # Check if all inputs are numbers
        if not ip.isdigit():
            mesg_string = 'All values input should be numbers'
            return False, mesg_string
            
        # Check if the first digit is not 0
        if int(ip[0]) == 0:
            mesg_string = "The first value shouldn't be zero"
            return False, mesg_string
            
        # Check for duplicate digits
        for i in range(len(ip)):
            if ip.count(ip[i]) > 1:
                mesg_string = "There shouldn't be a number that occurs twice"
                return False, mesg_string
                
        return True, None

    def get_input(self, x: str) -> Tuple[bool, Optional[Union[int, str]], Optional[str]]:
        """Process and validate user input.
        
        Args:
            x: The user's raw input string.
            
        Returns:
            A tuple of (is_valid, processed_value, error_message).
            processed_value is 'e' for exit, an int for valid guess, or None if invalid.
        """
        if x == 'e':
            return False, 'e', None
            
        flag, mesg_string = self.check_input(x)
        if not flag:
            return False, None, mesg_string
        return True, int(x), None

    def generate_number(self) -> int:
        """Generate a random number that satisfies game rules.
        
        Returns:
            A valid random number with no duplicate digits and not starting with 0.
        """
        min_val = 10 ** (self.digit_count - 1)
        max_val = (10 ** self.digit_count) - 1
        
        while True:
            num = random.randint(min_val, max_val)
            is_valid, _ = self.check_input(str(num))
            if is_valid:
                return num

    def compare(self, ip: int) -> Tuple[int, int]:
        """Compare a guess against the secret number.
        
        Args:
            ip: The player's guess as an integer.
            
        Returns:
            A tuple of (count, place) where:
            - count: How many digits from the guess exist in the secret number
            - place: How many of those digits are in the correct position
        """
        ref_n = str(self.num)
        ip_s = str(ip)
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

    def get_hint(self) -> Tuple[int, str]:
        """Reveal one digit of the secret number as a hint.
        
        Returns:
            A tuple of (position, digit) for the revealed hint.
        """
        num_str = str(self.num)
        position = self.hints_used % self.digit_count
        self.hints_used += 1
        return position, num_str[position]
