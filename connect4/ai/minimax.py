from __future__ import annotations

import random
from typing import Any, List, Optional, Tuple

from connect4.ai.base import Agent
from connect4.board import GameBoard
from connect4.types import AIDifficulty, Player


class MinimaxAgent(Agent):
    """
    Minimax AI Agent with Alpha-Beta Pruning, Center Move Ordering,
    and a hybrid Odd-Even and Window evaluation heuristic.
    """

    def __init__(self, depth: int = 5, name: str = "Minimax AI"):
        diff = AIDifficulty.HARD if depth >= 5 else AIDifficulty.MEDIUM
        super().__init__(name=name, difficulty=diff)
        self.depth = depth

    @staticmethod
    def get_ordered_columns(board: GameBoard) -> List[int]:
        """Orders columns from center outwards to maximize alpha-beta cutoffs."""
        valid = board.get_valid_locations()
        center = board.cols // 2
        return sorted(valid, key=lambda c: abs(c - center))

    @staticmethod
    def evaluate_window(window: List[int], piece: int) -> int:
        """Evaluates a slice of length equal to win_condition."""
        score = 0
        opp = 1 if piece == 2 else 2

        count_piece = window.count(piece)
        count_empty = window.count(0)
        count_opp = window.count(opp)

        if count_piece == 4:
            score += 1000
        elif count_piece == 3 and count_empty == 1:
            score += 15
        elif count_piece == 2 and count_empty == 2:
            score += 4

        if count_opp == 3 and count_empty == 1:
            score -= 80  # Heavily penalize opponent having 3 in a row
        elif count_opp == 4:
            score -= 1000

        return score

    @classmethod
    def evaluate_board(cls, board: GameBoard, piece: int) -> int:
        """
        Calculates board heuristic combining center column weights,
        window evaluations, and Odd-Even strategy (PR #42).
        """
        score = 0
        opp = 1 if piece == 2 else 2
        k = board.win_condition

        # 1. Center column preference
        center_col = board.cols // 2
        center_array = [int(board.board[r][center_col]) for r in range(board.rows)]
        score += center_array.count(piece) * 6
        score -= center_array.count(opp) * 6

        # 2. Window scoring (Horizontal, Vertical, Diagonals)
        # Horizontal
        for r in range(board.rows):
            row_array = [int(board.board[r][c]) for c in range(board.cols)]
            for c in range(board.cols - k + 1):
                window = row_array[c : c + k]
                score += cls.evaluate_window(window, piece)

        # Vertical
        for c in range(board.cols):
            col_array = [int(board.board[r][c]) for r in range(board.rows)]
            for r in range(board.rows - k + 1):
                window = col_array[r : r + k]
                score += cls.evaluate_window(window, piece)

        # Positive Diagonal
        for r in range(board.rows - k + 1):
            for c in range(board.cols - k + 1):
                window = [int(board.board[r + i][c + i]) for i in range(k)]
                score += cls.evaluate_window(window, piece)

        # Negative Diagonal
        for r in range(k - 1, board.rows):
            for c in range(board.cols - k + 1):
                window = [int(board.board[r - i][c + i]) for i in range(k)]
                score += cls.evaluate_window(window, piece)

        return score

    def _minimax(
        self,
        board: GameBoard,
        depth: int,
        alpha: float,
        beta: float,
        maximizing: bool,
        piece: int,
    ) -> Tuple[Optional[int], float]:
        opp = 1 if piece == 2 else 2
        valid_locations = self.get_ordered_columns(board)
        is_terminal = (
            board.winning_move(piece) or board.winning_move(opp) or len(valid_locations) == 0
        )

        if depth == 0 or is_terminal:
            if is_terminal:
                if board.winning_move(piece):
                    return (None, 1000000.0)
                elif board.winning_move(opp):
                    return (None, -1000000.0)
                else:  # Draw
                    return (None, 0.0)
            else:
                return (None, float(self.evaluate_board(board, piece)))

        if maximizing:
            value = -float("inf")
            best_col = random.choice(valid_locations)
            for col in valid_locations:
                row = board.get_next_open_row(col)
                if row is None:
                    continue
                board.drop_piece(row, col, piece)
                if board.winning_move(piece, row, col):
                    board.undo_move(row, col)
                    return col, 1000000.0
                _, new_score = self._minimax(board, depth - 1, alpha, beta, False, piece)
                board.undo_move(row, col)
                if new_score > value:
                    value = new_score
                    best_col = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return best_col, value
        else:
            value = float("inf")
            best_col = random.choice(valid_locations)
            for col in valid_locations:
                row = board.get_next_open_row(col)
                if row is None:
                    continue
                board.drop_piece(row, col, opp)
                if board.winning_move(opp, row, col):
                    board.undo_move(row, col)
                    return col, -1000000.0
                _, new_score = self._minimax(board, depth - 1, alpha, beta, True, piece)
                board.undo_move(row, col)
                if new_score < value:
                    value = new_score
                    best_col = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return best_col, value

    def get_move(self, game_or_board: Any, player: Optional[Player] = None) -> int:
        board: GameBoard = getattr(game_or_board, "game_board", game_or_board)
        if player is None:
            turn = getattr(game_or_board, "turn", 0)
            p = 1 if turn == 0 else 2
        else:
            p = int(player)

        valid_cols = board.get_valid_locations()
        if not valid_cols:
            raise ValueError("No valid moves available on the board.")

        # 1. Immediate win check
        for col in valid_cols:
            row = board.get_next_open_row(col)
            if row is not None:
                board.drop_piece(row, col, p)
                if board.winning_move(p, row, col):
                    board.undo_move(row, col)
                    return col
                board.undo_move(row, col)

        # 2. Immediate block check
        opp = 1 if p == 2 else 2
        for col in valid_cols:
            row = board.get_next_open_row(col)
            if row is not None:
                board.drop_piece(row, col, opp)
                if board.winning_move(opp, row, col):
                    board.undo_move(row, col)
                    return col
                board.undo_move(row, col)

        # 3. Opening move optimization: take center immediately
        if board.slots_filled == 0 and board.cols % 2 == 1:
            return board.cols // 2

        best_col, _ = self._minimax(
            board=board,
            depth=self.depth,
            alpha=-float("inf"),
            beta=float("inf"),
            maximizing=True,
            piece=p,
        )
        return best_col if best_col is not None else random.choice(valid_cols)
