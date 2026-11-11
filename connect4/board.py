from __future__ import annotations

from typing import Any, Dict, List, Optional, Set, Tuple
import numpy as np
from numpy import flip, zeros, ndarray

from connect4.types import BoardDimensions, Player


class GameBoard:
    """
    High-performance GameBoard representation for Connect 4 and generalized Connect-N.
    Manages grid state, move mechanics, win detection, and heuristic evaluation squares.
    """

    board: ndarray
    rows: int
    cols: int
    win_condition: int
    slots_filled: int

    def __init__(self, rows: int = 6, cols: int = 7, win_condition: int = 4):
        """
        Initializes the board grid.
        :param rows: Height of grid in rows (standard 6).
        :param cols: Width of grid in columns (standard 7).
        :param win_condition: Consecutive chips needed to win (standard 4).
        """
        self.rows = int(rows)
        self.cols = int(cols)
        self.win_condition = int(win_condition)
        self.board = zeros((self.rows, self.cols), dtype=int)
        self.slots_filled = 0
        self.p1_win_squares: Set[Tuple[int, int]] = set()
        self.p2_win_squares: Set[Tuple[int, int]] = set()

    @property
    def dimensions(self) -> BoardDimensions:
        return BoardDimensions(cols=self.cols, rows=self.rows, win_condition=self.win_condition)

    def print_board(self) -> None:
        """Prints the visual state of the board in the terminal."""
        print(flip(self.board, 0))
        print(" " + "-" * (self.cols * 3))
        print(" " + str([c + 1 for c in range(self.cols)]))

    def drop_piece(self, row: int, col: int, piece: int) -> None:
        """
        Drops or places a piece into the specified coordinate slot.
        """
        old_val = self.board[row][col]
        self.board[row][col] = piece
        if old_val == 0 and piece != 0:
            self.slots_filled += 1
        elif old_val != 0 and piece == 0:
            self.slots_filled = max(0, self.slots_filled - 1)

    def undo_move(self, row: int, col: int) -> None:
        """Clears a move from the board."""
        if self.board[row][col] != 0:
            self.board[row][col] = 0
            self.slots_filled = max(0, self.slots_filled - 1)

    def is_valid_location(self, col: int) -> bool:
        """
        Checks if a column is in bounds and not full.
        """
        if col < 0 or col >= self.cols:
            return False
        return bool(self.board[self.rows - 1][col] == 0)

    def is_valid_coord(self, r: int, c: int) -> bool:
        """Validates if coordinates are within the board bounds."""
        return 0 <= r < self.rows and 0 <= c < self.cols

    def get_valid_locations(self) -> List[int]:
        """Returns list of open column indices."""
        return [c for c in range(self.cols) if self.is_valid_location(c)]

    def get_next_open_row(self, col: int) -> Optional[int]:
        """
        Returns the lowest empty row in the column, or None if full.
        """
        if not self.is_valid_location(col):
            return None
        for r in range(self.rows):
            if self.board[r][col] == 0:
                return r
        return None

    def check_square(self, piece: int, r: int, c: int) -> bool:
        """Checks if board[r][c] equals piece safely."""
        if not self.is_valid_coord(r, c):
            return False
        return bool(self.board[r][c] == piece)

    def horizontal_win(self, piece: int, r: int, c: int) -> bool:
        """Checks for consecutive chips horizontally starting at (r, c)."""
        k = self.win_condition
        if c + k > self.cols:
            return False
        return all(self.board[r][c + i] == piece for i in range(k))

    def vertical_win(self, piece: int, r: int, c: int) -> bool:
        """Checks for consecutive chips vertically starting at (r, c)."""
        k = self.win_condition
        if r + k > self.rows:
            return False
        return all(self.board[r + i][c] == piece for i in range(k))

    def diagonal_win(self, piece: int, r: int, c: int) -> bool:
        """Checks for positive and negative diagonal wins starting at (r, c)."""
        k = self.win_condition
        # Positive diagonal (up-right)
        pos = True
        if r + k <= self.rows and c + k <= self.cols:
            for i in range(k):
                if self.board[r + i][c + i] != piece:
                    pos = False
                    break
        else:
            pos = False

        if pos:
            return True

        # Negative diagonal (down-right)
        neg = True
        if r - k + 1 >= 0 and c + k <= self.cols:
            for i in range(k):
                if self.board[r - i][c + i] != piece:
                    neg = False
                    break
        else:
            neg = False

        return neg

    def winning_move(self, piece: int, r: Optional[int] = None, c: Optional[int] = None) -> bool:
        """
        Checks if player with `piece` has won.
        If `r` and `c` are specified, performs localized directional check around (r, c) in O(K).
        Otherwise performs full board sweep in O(R * C).
        """
        k = self.win_condition
        piece = int(piece)

        if r is not None and c is not None and self.is_valid_coord(r, c):
            # Optimized localized win check in 4 directions around (r, c)
            directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
            for dr, dc in directions:
                count = 1
                # Forward direction
                step = 1
                while self.check_square(piece, r + step * dr, c + step * dc):
                    count += 1
                    step += 1
                # Backward direction
                step = 1
                while self.check_square(piece, r - step * dr, c - step * dc):
                    count += 1
                    step += 1
                if count >= k:
                    return True
            return False

        # Full board sweep fallback
        # Horizontal
        for row in range(self.rows):
            for col in range(self.cols - k + 1):
                if all(self.board[row][col + i] == piece for i in range(k)):
                    return True

        # Vertical
        for col in range(self.cols):
            for row in range(self.rows - k + 1):
                if all(self.board[row + i][col] == piece for i in range(k)):
                    return True

        # Positive diagonal
        for row in range(self.rows - k + 1):
            for col in range(self.cols - k + 1):
                if all(self.board[row + i][col + i] == piece for i in range(k)):
                    return True

        # Negative diagonal
        for row in range(k - 1, self.rows):
            for col in range(self.cols - k + 1):
                if all(self.board[row - i][col + i] == piece for i in range(k)):
                    return True

        return False

    def get_winning_coordinates(self, piece: int) -> Optional[List[Tuple[int, int]]]:
        """
        Finds the exact list of coordinates forming the winning connection.
        Useful for highlighting winning moves in UI and terminal.
        """
        k = self.win_condition
        piece = int(piece)

        # Horizontal
        for row in range(self.rows):
            for col in range(self.cols - k + 1):
                if all(self.board[row][col + i] == piece for i in range(k)):
                    return [(row, col + i) for i in range(k)]

        # Vertical
        for col in range(self.cols):
            for row in range(self.rows - k + 1):
                if all(self.board[row + i][col] == piece for i in range(k)):
                    return [(row + i, col) for i in range(k)]

        # Positive diagonal
        for row in range(self.rows - k + 1):
            for col in range(self.cols - k + 1):
                if all(self.board[row + i][col + i] == piece for i in range(k)):
                    return [(row + i, col + i) for i in range(k)]

        # Negative diagonal
        for row in range(k - 1, self.rows):
            for col in range(self.cols - k + 1):
                if all(self.board[row - i][col + i] == piece for i in range(k)):
                    return [(row - i, col + i) for i in range(k)]

        return None

    def tie_move(self) -> bool:
        """
        Checks if the game has ended in a draw (board full and no winning move).
        """
        if self.slots_filled < self.rows * self.cols:
            return False
        return not self.winning_move(1) and not self.winning_move(2)

    def is_full(self) -> bool:
        """Checks if the board has no empty spaces remaining."""
        return self.slots_filled >= (self.rows * self.cols)

    def copy(self) -> GameBoard:
        """Creates an independent fast copy of this board."""
        clone = GameBoard(self.rows, self.cols, self.win_condition)
        clone.board = np.copy(self.board)
        clone.slots_filled = self.slots_filled
        clone.p1_win_squares = set(self.p1_win_squares)
        clone.p2_win_squares = set(self.p2_win_squares)
        return clone

    def clear(self) -> None:
        """Resets the board state to all zeros."""
        self.board.fill(0)
        self.slots_filled = 0
        self.p1_win_squares.clear()
        self.p2_win_squares.clear()

    def update_win_squares(self) -> None:
        """
        Calculates and stores squares where a player would immediately complete a win
        (used by Odd-Even heuristic in MinimaxAgent).
        """
        self.p1_win_squares.clear()
        self.p2_win_squares.clear()

        for c in range(self.cols):
            for r in range(self.rows):
                if self.board[r][c] == 0:
                    # Test P1
                    self.board[r][c] = 1
                    if self.winning_move(1, r, c):
                        self.p1_win_squares.add((r, c))
                    # Test P2
                    self.board[r][c] = 2
                    if self.winning_move(2, r, c):
                        self.p2_win_squares.add((r, c))
                    self.board[r][c] = 0

    def to_dict(self) -> Dict[str, Any]:
        """Serializes board state to dictionary representation."""
        return {
            "rows": self.rows,
            "cols": self.cols,
            "win_condition": self.win_condition,
            "slots_filled": self.slots_filled,
            "grid": self.board.tolist(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> GameBoard:
        """Deserializes board state from dictionary."""
        board = cls(
            rows=data.get("rows", 6),
            cols=data.get("cols", 7),
            win_condition=data.get("win_condition", 4)
        )
        grid = np.array(data.get("grid", []), dtype=int)
        if grid.shape == (board.rows, board.cols):
            board.board = grid
            board.slots_filled = int(np.count_nonzero(board.board))
        return board
