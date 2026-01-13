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
python main.py
```

### Command Line Version
```bash
python -m numbers_game.ui.cli
```

## 🎮 Game Modes

| Mode | Description |
|------|-------------|
| **1 Player** | Guess the computer's random number |
| **2 Players** | Each player sets a secret number for the other to guess. Fair play: if one cracks the code, the other gets one final guess! |
| **Online** | Play over LAN - one hosts, the other joins by IP |

## 🏆 Difficulty Levels

| Level | Digits | Range |
|-------|--------|-------|
| Easy | 4 | 1000-9999 |
| Medium | 5 | 10000-99999 |
| Hard | 6 | 100000-999999 |

## 📁 Project Structure

```
python3/
├── main.py                    # GUI entry point
├── gui_numbers_game.py        # Main GUI implementation
├── numbers_game/              # Main package
│   ├── core/                  # Game logic
│   │   ├── engine.py         # GameEngine class
│   │   └── high_scores.py    # Score persistence
│   ├── network/               # Online multiplayer
│   │   └── manager.py        # NetworkManager class
│   ├── ui/                    # User interfaces
│   │   ├── cli.py            # CLI version
│   │   └── thinking_area.py  # Helper window
│   └── utils/                 # Utilities
│       └── help_text.py      # Game instructions
├── tests/                     # Unit tests (18 tests)
│   └── test_engine.py
├── build_windows.bat          # Build Windows executable
└── build_linux.sh             # Build Linux executable
```

## 🧪 Running Tests

```bash
pytest tests/test_engine.py -v
```

## � Building Standalone Executables

### Windows
```bash
# Install PyInstaller
pip install pyinstaller

# Build (or run build_windows.bat)
pyinstaller --onefile --windowed --name "NumbersGame" --add-data "numbers_game;numbers_game" main.py
```
Executable: `dist/NumbersGame.exe`

### Ubuntu/Linux
```bash
# Install dependencies
sudo apt-get install python3-pip python3-tk
pip3 install pyinstaller ttkbootstrap

# Build (or run build_linux.sh)
pyinstaller --onefile --windowed --name "NumbersGame" --add-data "numbers_game:numbers_game" main.py
```
Executable: `dist/NumbersGame`

## �👤 Author

Ahmed Essam El Fakharany - afakharany93@gmail.com
