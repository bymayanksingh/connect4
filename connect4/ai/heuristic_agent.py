from __future__ import annotations

import random
from typing import Any, List, Optional

from connect4.ai.base import Agent
from connect4.board import GameBoard
from connect4.types import AIDifficulty, Player


class HeuristicAgent(Agent):
    """
    Fast rule-based AI agent (Easy / Medium):
    1. Plays immediate winning moves.
    2. Blocks opponent immediate wins.
    3. Avoids creating winning opportunities directly above for the opponent.
    4. Prefers central columns to maximize future connectivity.
    """

    def __init__(self, name: str = "Heuristic AI"):
        super().__init__(name=name, difficulty=AIDifficulty.EASY)

    def get_move(self, game_or_board: Any, player: Optional[Player] = None) -> int:
        board: GameBoard = getattr(game_or_board, "game_board", game_or_board)
        if player is None:
            # Try to infer from game_data turn (0 -> P1, 1 -> P2)
            turn = getattr(game_or_board, "turn", 0)
            p = Player.P1 if turn == 0 else Player.P2
        else:
            p = player

        opp = p.opponent
        valid_cols = board.get_valid_locations()
        if not valid_cols:
            raise ValueError("No valid moves available on the board.")

        # 1. Immediate win check
        for col in valid_cols:
            row = board.get_next_open_row(col)
            if row is not None:
                board.drop_piece(row, col, int(p))
                if board.winning_move(int(p), row, col):
                    board.undo_move(row, col)
                    return col
                board.undo_move(row, col)

        # 2. Immediate block check
        for col in valid_cols:
            row = board.get_next_open_row(col)
            if row is not None:
                board.drop_piece(row, col, int(opp))
                if board.winning_move(int(opp), row, col):
                    board.undo_move(row, col)
                    return col
                board.undo_move(row, col)

        # 3. Filter moves that don't immediately gift a win to opponent on the row above
        safe_moves: List[int] = []
        for col in valid_cols:
            row = board.get_next_open_row(col)
            if row is not None:
                board.drop_piece(row, col, int(p))
                next_row = board.get_next_open_row(col)
                gifts_win = False
                if next_row is not None:
                    board.drop_piece(next_row, col, int(opp))
                    if board.winning_move(int(opp), next_row, col):
                        gifts_win = True
                    board.undo_move(next_row, col)
                board.undo_move(row, col)
                if not gifts_win:
                    safe_moves.append(col)

        candidate_pool = safe_moves if safe_moves else valid_cols

        # 4. Prefer center columns
        center = board.cols // 2
        candidate_pool.sort(key=lambda c: abs(c - center))
        # Choose among best centered candidates
        best_dist = abs(candidate_pool[0] - center)
        best_candidates = [c for c in candidate_pool if abs(c - center) == best_dist]
        return random.choice(best_candidates)
