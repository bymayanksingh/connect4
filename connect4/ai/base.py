from __future__ import annotations

import abc
from typing import Any, Optional

from connect4.types import AIDifficulty, Player


class Agent(abc.ABC):
    """
    Abstract Base Class for Connect 4 AI agents.
    """

    name: str
    difficulty: AIDifficulty

    def __init__(self, name: str = "AI", difficulty: AIDifficulty = AIDifficulty.MEDIUM):
        self.name = name
        self.difficulty = difficulty

    @abc.abstractmethod
    def get_move(self, game_or_board: Any, player: Optional[Player] = None) -> int:
        """
        Determines the best valid column move for the current player.
        :param game_or_board: Game instance or GameBoard.
        :param player: The player making the move (Player.P1 or Player.P2).
        :return: Selected 0-indexed column integer.
        """
        pass
