# 🎮 Numbers Discovery Game

A number guessing game where you try to guess a randomly generated number in the fewest attempts possible.

## 🎯 How to Play

1. The computer generates a secret number (4-6 digits based on difficulty)
2. You guess numbers and receive feedback in the format `X/Y`:
   - **X** = How many digits from your guess exist in the secret number
   - **Y** = How many of those digits are in the correct position
3. Keep guessing until you get all digits correct (`5/5` for medium difficulty)

### Example

If the secret number is `28461` and you guess `26798`:
- Reply: **`3/1`**
  - 3 digits exist (`2`, `6`, `8`)
  - 1 is in the correct position (the `2`)

## 📦 Installation

```bash
# Create conda environment
conda create -n numbers_game python=3.11
conda activate numbers_game

# Navigate to project
cd path/to/Numbers-game-master/python3
```

## ▶️ Running the Game

### Command Line Version
```bash
python cli_numbers_game.py
```

### GUI Version
```bash
python gui_numbers_game.py
```

## 🎮 Commands

| Command | Action |
|---------|--------|
| `e` | Exit and reveal the answer |
| `h` | Get a hint (costs 5 points) |
| `r` | Restart the current game |

## 🏆 Difficulty Levels

| Level | Digits | Range |
|-------|--------|-------|
| Easy | 4 | 1000-9999 |
| Medium | 5 | 10000-99999 |
| Hard | 6 | 100000-999999 |

## 📁 Project Structure

```
python3/
├── game_engine.py      # Core game logic
├── cli_numbers_game.py # Command-line interface
├── gui_numbers_game.py # Tkinter GUI
├── help_string.py      # Game instructions
├── high_scores.py      # Score persistence
└── test_game_engine.py # Unit tests
```

## 👤 Author

Ahmed Essam El Fakharany - afakharany93@gmail.com
