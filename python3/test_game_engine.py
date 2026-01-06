"""Unit tests for the Numbers Game engine."""

import pytest
from game_engine import NumGame, DEFAULT_DIGIT_COUNT


class TestNumGameInit:
    """Tests for NumGame initialization."""
    
    def test_default_digit_count(self):
        """Test that default game has 5 digits."""
        game = NumGame()
        assert game.digit_count == 5
        
    def test_custom_digit_count(self):
        """Test custom digit count initialization."""
        game = NumGame(digit_count=4)
        assert game.digit_count == 4
        
    def test_generated_number_length(self):
        """Test that generated number has correct length."""
        for digits in [4, 5, 6]:
            game = NumGame(digit_count=digits)
            assert len(str(game.num)) == digits


class TestCheckInput:
    """Tests for input validation."""
    
    def test_valid_input(self):
        """Test valid 5-digit number."""
        game = NumGame()
        is_valid, msg = game.check_input("12345")
        assert is_valid is True
        assert msg is None
        
    def test_wrong_length(self):
        """Test rejection of wrong length input."""
        game = NumGame()
        is_valid, msg = game.check_input("1234")
        assert is_valid is False
        assert "not 5 digits" in msg
        
    def test_non_numeric(self):
        """Test rejection of non-numeric input."""
        game = NumGame()
        is_valid, msg = game.check_input("1234a")
        assert is_valid is False
        assert "numbers" in msg.lower()
        
    def test_leading_zero(self):
        """Test rejection of leading zero."""
        game = NumGame()
        is_valid, msg = game.check_input("01234")
        assert is_valid is False
        assert "zero" in msg.lower()
        
    def test_duplicate_digits(self):
        """Test rejection of duplicate digits."""
        game = NumGame()
        is_valid, msg = game.check_input("11234")
        assert is_valid is False
        assert "twice" in msg.lower()


class TestCompare:
    """Tests for number comparison logic."""
    
    def test_exact_match(self):
        """Test exact match returns full count and place."""
        game = NumGame()
        game.num = 12345
        count, place = game.compare(12345)
        assert count == 5
        assert place == 5
        
    def test_no_match(self):
        """Test no matching digits."""
        game = NumGame()
        game.num = 12345
        count, place = game.compare(67890)
        assert count == 0
        assert place == 0
        
    def test_partial_match_wrong_position(self):
        """Test digits exist but in wrong positions."""
        game = NumGame()
        game.num = 12345
        count, place = game.compare(54321)
        assert count == 5
        assert place == 1  # Only '3' is in correct position
        
    def test_some_matching(self):
        """Test some digits matching."""
        game = NumGame()
        game.num = 28461
        count, place = game.compare(26798)
        assert count == 3  # 2, 6, 8 match
        assert place == 1  # Only 2 is in correct position


class TestGenerateNumber:
    """Tests for number generation."""
    
    def test_no_leading_zero(self):
        """Test generated numbers don't start with zero."""
        for _ in range(10):
            game = NumGame()
            assert str(game.num)[0] != '0'
            
    def test_no_duplicate_digits(self):
        """Test generated numbers have no duplicate digits."""
        for _ in range(10):
            game = NumGame()
            num_str = str(game.num)
            assert len(num_str) == len(set(num_str))
            
    def test_number_in_valid_range(self):
        """Test generated numbers are in valid range."""
        game = NumGame(digit_count=5)
        assert 10000 <= game.num <= 99999
        
        game4 = NumGame(digit_count=4)
        assert 1000 <= game4.num <= 9999


class TestGetHint:
    """Tests for hint functionality."""
    
    def test_hint_returns_valid_digit(self):
        """Test hint returns a valid position and digit."""
        game = NumGame()
        game.num = 12345
        position, digit = game.get_hint()
        assert position == 0
        assert digit == '1'
        
    def test_hints_cycle_through_positions(self):
        """Test hints reveal different positions."""
        game = NumGame()
        game.num = 12345
        positions = []
        for _ in range(5):
            pos, _ = game.get_hint()
            positions.append(pos)
        assert positions == [0, 1, 2, 3, 4]


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
