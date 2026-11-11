"""
Connect 4: Production-Grade Game, AI Engine & Visualizer.
"""

from connect4.board import GameBoard
from connect4.game import Connect4Game
from connect4.types import (
    BoardDimensions,
    GameMode,
    GameStatus,
    MoveResult,
    Player,
    AIDifficulty,
)
from connect4.ai.factory import AgentFactory
from connect4.visualizer.export import Visualizer

__version__ = "2.0.0"

__all__ = [
    "GameBoard",
    "Connect4Game",
    "BoardDimensions",
    "GameMode",
    "GameStatus",
    "MoveResult",
    "Player",
    "AIDifficulty",
    "AgentFactory",
    "Visualizer",
    "__version__",
]
