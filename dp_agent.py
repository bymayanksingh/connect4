"""
Backward compatibility layer for legacy dp_agent.py.
For modern development, import directly from connect4.ai.
"""
from connect4.ai.dp_agent import DPAgent, GameBoard, GameState

__all__ = ["DPAgent", "GameBoard", "GameState"]
