# 🎮 Numbers Discovery Game

A number guessing game where you try to guess a randomly generated number in the fewest attempts possible.

## 🎯 How to Play

1. The computer generates a secret number (4-6 digits based on difficulty)
2. You guess numbers and receive feedback in the format `X/Y`:
   - **X** = How many digits from your guess exist in the secret number
   - **Y** = How many of those digits are in the correct position
3. Keep guessing until you get all digits correct

### Example

If the secret number is `28461` and you guess `26798`:
- Reply: **`3/1`** (3 digits exist, 1 in correct position)

## 📦 Installation

```bash
# Create conda environment
conda create -n numbers_game python=3.11
conda activate numbers_game

# Install dependencies
pip install -r requirements.txt
```

## ▶️ Running the Game

### GUI Version (Recommended)
```bash
python gui_numbers_game.py
```

### Command Line Version
```bash
python cli_numbers_game.py
```

## 🎮 Game Modes

| Mode | Description |
|------|-------------|
| **1 Player** | Guess the computer's random number |
| **2 Players** | Each player sets a secret number for the other to guess. First to crack wins! Split-screen view shows each player's progress. |

## 🏆 Difficulty Levels

| Level | Digits | Range |
|-------|--------|-------|
| Easy | 4 | 1000-9999 |
| Medium | 5 | 10000-99999 |
| Hard | 6 | 100000-999999 |

## 🎮 Commands (CLI)

| Command | Action |
|---------|--------|
| `e` | Exit and reveal the answer |
| `h` | Get a hint (costs 5 points) |
| `r` | Restart the current game |

## 📁 Project Structure

```
python3/
├── game_engine.py      # Core game logic
├── cli_numbers_game.py # Command-line interface
├── gui_numbers_game.py # Modern Tkinter GUI
├── help_string.py      # Game instructions
├── high_scores.py      # Score persistence
└── test_game_engine.py # Unit tests (17 tests)
```

## 🧪 Running Tests

```bash
pytest test_game_engine.py -v
```

## 👤 Author

Ahmed Essam El Fakharany - afakharany93@gmail.com
