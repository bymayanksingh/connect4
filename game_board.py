"""
Backward compatibility layer for legacy game_board.py.
For modern development, import directly from connect4.board.
"""
from connect4.board import GameBoard

__all__ = ["GameBoard"]
