@echo off
REM Build script for Windows
REM Creates a standalone .exe file

echo Building Numbers Game for Windows...

REM Activate conda environment (adjust if needed)
call conda activate numbers_game

REM Build the executable
pyinstaller --onefile --windowed --name "NumbersGame" --add-data "numbers_game;numbers_game" main.py

echo.
echo Build complete! Executable is at: dist\NumbersGame.exe
pause
