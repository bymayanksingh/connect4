"""
Connect Four: Production-Grade Desktop Application Launcher.

Usage:
    python game.py              # Launch interactive Pygame GUI
    python -m connect4          # Launch interactive terminal mode
    python -m connect4 --help   # Display CLI options and tournament runner
"""

from connect4.gui.app import run_gui

if __name__ == "__main__":
    run_gui()
