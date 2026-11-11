"""
Backward compatibility layer for legacy game_state.py.
For modern development, import directly from connect4.ai.
"""
from connect4.ai.game_state import GameState

__all__ = ["GameState"]
