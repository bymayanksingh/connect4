"""
Connect Four Entry Point (GUI & Backward Compatibility).

To play via GUI:
    python game.py

To play via Terminal / CLI:
    python -m connect4
"""
import sys
from connect4.gui.app import Connect4App, run_gui
from connect4.game import Connect4Game
from connect4.board import GameBoard
from connect4.types import BoardDimensions, GameMode, Player

def start(mode: str = 'pvp', board_size: tuple = None):
    """Legacy start function."""
    app = Connect4App()
    if board_size:
        cols, rows, win_condition = board_size
        app.dimensions = BoardDimensions(cols=cols, rows=rows, win_condition=win_condition)
    if mode in ('pvp', 'pva', 'ava'):
        app.mode = GameMode(mode)
    app.start_game()
    app.run()

def quit():
    sys.exit(0)

if __name__ == '__main__':
    run_gui()
