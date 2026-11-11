from __future__ import annotations

from typing import Any, Dict, List, Optional

from connect4.ai.base import Agent
from connect4.board import GameBoard
from connect4.types import (
    BoardDimensions,
    GameMode,
    GameStatus,
    MoveResult,
    Player,
)


class Connect4Game:
    """
    Core game session coordinator.
    Decoupled from Pygame rendering and terminal I/O, maintaining strict
    game rules, state transitions, move history, and AI integration.
    """

    board: GameBoard
    current_player: Player
    mode: GameMode
    status: GameStatus
    agent1: Optional[Agent]
    agent2: Optional[Agent]
    move_history: List[MoveResult]
    redo_history: List[MoveResult]

    def __init__(
        self,
        board: Optional[GameBoard] = None,
        dimensions: Optional[BoardDimensions] = None,
        mode: GameMode = GameMode.PVP,
        agent1: Optional[Agent] = None,
        agent2: Optional[Agent] = None,
    ):
        if board is not None:
            self.board = board
        elif dimensions is not None:
            self.board = GameBoard(
                rows=dimensions.rows,
                cols=dimensions.cols,
                win_condition=dimensions.win_condition,
            )
        else:
            self.board = GameBoard(rows=6, cols=7, win_condition=4)

        self.current_player = Player.P1
        self.mode = mode
        self.status = GameStatus.IN_PROGRESS
        self.agent1 = agent1
        self.agent2 = agent2
        self.move_history = []
        self.redo_history = []

    @property
    def is_game_over(self) -> bool:
        return self.status != GameStatus.IN_PROGRESS

    @property
    def winner(self) -> Optional[Player]:
        if self.status == GameStatus.WIN_P1:
            return Player.P1
        elif self.status == GameStatus.WIN_P2:
            return Player.P2
        return None

    @property
    def turn(self) -> int:
        """0 for Player 1, 1 for Player 2 (backward compatibility)."""
        return 0 if self.current_player == Player.P1 else 1

    @turn.setter
    def turn(self, val: int) -> None:
        self.current_player = Player.P1 if val == 0 else Player.P2

    @property
    def game_board(self) -> GameBoard:
        """Backward compatibility alias."""
        return self.board

    def make_move(self, col: int) -> MoveResult:
        """
        Executes a move in the specified column for the current player.
        Raises ValueError if column is invalid or full, or RuntimeError if game is already over.
        """
        if self.is_game_over:
            raise RuntimeError("Cannot make move: game is already over.")

        if not self.board.is_valid_location(col):
            raise ValueError(f"Column {col} is full or out of bounds (0..{self.board.cols - 1}).")

        row = self.board.get_next_open_row(col)
        if row is None:
            raise ValueError(f"Column {col} is full.")

        player = self.current_player
        self.board.drop_piece(row, col, int(player))

        # Check win or tie
        is_win = self.board.winning_move(int(player), row, col)
        is_draw = False
        winning_coords = None

        if is_win:
            self.status = GameStatus.WIN_P1 if player == Player.P1 else GameStatus.WIN_P2
            winning_coords = self.board.get_winning_coordinates(int(player))
        elif self.board.tie_move():
            self.status = GameStatus.DRAW
            is_draw = True
        else:
            # Advance turn
            self.current_player = player.opponent

        result = MoveResult(
            row=row,
            col=col,
            player=player,
            is_win=is_win,
            is_draw=is_draw,
            winning_coords=winning_coords,
        )

        self.move_history.append(result)
        self.redo_history.clear()
        return result

    def undo(self) -> Optional[MoveResult]:
        """
        Rolls back the most recent move.
        In PvA mode, automatically rolls back both the AI's move and the human's move
        if it is currently human's turn.
        """
        if not self.move_history:
            return None

        last_move = self.move_history.pop()
        self.board.undo_move(last_move.row, last_move.col)
        self.current_player = last_move.player
        self.status = GameStatus.IN_PROGRESS
        self.redo_history.append(last_move)
        return last_move

    def redo(self) -> Optional[MoveResult]:
        """Re-applies the most recently undone move."""
        if not self.redo_history:
            return None

        move = self.redo_history.pop()
        self.board.drop_piece(move.row, move.col, int(move.player))

        if move.is_win:
            self.status = GameStatus.WIN_P1 if move.player == Player.P1 else GameStatus.WIN_P2
        elif move.is_draw:
            self.status = GameStatus.DRAW
        else:
            self.current_player = move.player.opponent

        self.move_history.append(move)
        return move

    def restart(self) -> None:
        """Resets the game state and board while keeping configurations."""
        self.board.clear()
        self.current_player = Player.P1
        self.status = GameStatus.IN_PROGRESS
        self.move_history.clear()
        self.redo_history.clear()

    def get_current_agent(self) -> Optional[Agent]:
        """Returns the Agent responsible for the current turn, if applicable."""
        if self.mode == GameMode.PVA and self.current_player == Player.P2:
            return self.agent2 or self.agent1
        elif self.mode == GameMode.AVA:
            return self.agent1 if self.current_player == Player.P1 else self.agent2
        return None

    def play_ai_turn(self) -> Optional[MoveResult]:
        """Queries the current AI agent and executes its move."""
        agent = self.get_current_agent()
        if agent is None or self.is_game_over:
            return None

        col = agent.get_move(self, self.current_player)
        return self.make_move(col)

    def to_dict(self) -> Dict[str, Any]:
        """Serializes current game state to a JSON-compatible dictionary."""
        return {
            "status": self.status.value,
            "current_player": self.current_player.value,
            "turn": self.turn,
            "mode": self.mode.value,
            "is_game_over": self.is_game_over,
            "winner": self.winner.value if self.winner else None,
            "total_moves": len(self.move_history),
            "board": self.board.to_dict(),
        }
