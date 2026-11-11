from __future__ import annotations

import random
from typing import Any, Optional

from connect4.ai.base import Agent
from connect4.board import GameBoard
from connect4.types import AIDifficulty, Player


class RandomAgent(Agent):
    """
    Selects uniformly at random among open valid columns.
    """

    def __init__(self, name: str = "Random AI"):
        super().__init__(name=name, difficulty=AIDifficulty.RANDOM)

    def get_move(self, game_or_board: Any, player: Optional[Player] = None) -> int:
        board: GameBoard = getattr(game_or_board, "game_board", game_or_board)
        valid_cols = board.get_valid_locations()
        if not valid_cols:
            raise ValueError("No valid moves available on the board.")
        return random.choice(valid_cols)
