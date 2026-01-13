#!/bin/bash
# Build script for Ubuntu/Linux
# Run this on an Ubuntu machine to create the Linux executable

# Prerequisites:
# sudo apt-get install python3-pip python3-tk
# pip3 install pyinstaller ttkbootstrap

echo "Building Numbers Game for Linux..."

# Navigate to script directory
cd "$(dirname "$0")"

# Build the executable
pyinstaller --onefile \
    --windowed \
    --name "NumbersGame" \
    --add-data "numbers_game:numbers_game" \
    main.py

echo ""
echo "Build complete! Executable is at: dist/NumbersGame"
echo "To run: ./dist/NumbersGame"
