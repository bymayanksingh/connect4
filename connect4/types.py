from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, IntEnum
from typing import List, Optional, Tuple


class Player(IntEnum):
    """Represents a player on the board."""

    NONE = 0
    P1 = 1
    P2 = 2

    @property
    def opponent(self) -> Player:
        if self == Player.P1:
            return Player.P2
        elif self == Player.P2:
            return Player.P1
        return Player.NONE

    @property
    def display_name(self) -> str:
        if self == Player.P1:
            return "Player 1 (Red)"
        elif self == Player.P2:
            return "Player 2 (Yellow)"
        return "None"


class GameMode(str, Enum):
    """Supported gameplay modes."""

    PVP = "pvp"  # Human vs Human
    PVA = "pva"  # Human vs AI
    AVA = "ava"  # AI vs AI (spectate / benchmark)


class AIDifficulty(str, Enum):
    """AI agent difficulty levels."""

    RANDOM = "random"  # Random moves (Very Easy)
    EASY = "easy"  # 1-ply immediate win/block heuristic
    MEDIUM = "medium"  # Minimax depth 3 with positional evaluation
    HARD = "hard"  # Minimax depth 5 with alpha-beta & odd-even heuristic
    EXPERT = "expert"  # Deep Dynamic Programming / MDP linear algebra agent


class GameStatus(str, Enum):
    """State of the game session."""

    IN_PROGRESS = "in_progress"
    WIN_P1 = "win_p1"
    WIN_P2 = "win_p2"
    DRAW = "draw"


@dataclass(frozen=True)
class BoardDimensions:
    """Configurable board dimensions and win condition."""

    cols: int = 7
    rows: int = 6
    win_condition: int = 4

    def is_standard(self) -> bool:
        return self.cols == 7 and self.rows == 6 and self.win_condition == 4


@dataclass
class MoveResult:
    """Details regarding the execution of a piece drop."""

    row: int
    col: int
    player: Player
    is_win: bool = False
    is_draw: bool = False
    winning_coords: Optional[List[Tuple[int, int]]] = None
