from numpy import flip, zeros
from numpy import ndarray
from typing import Set, Tuple


class GameBoard:
    """
    The GameBoard class holds the state of the game board,
    and methods to manipulate and query the board.
    """

    board: ndarray
    cols: int
    rows: int

    # Class variables to reduce the number of operations by remembering previous calculus
    # (specially useful for the AI agents):
    slots_filled: int
    # The squares where if a player had a piece would win the game
    p1_win_squares: Set[Tuple[int, int]]  # {(row, col), ...}
    p2_win_squares: Set[Tuple[int, int]]

    def __init__(self, rows=6, cols=7):
        """
        Initializes the game board.
        :param rows: The height of the board in rows.
        :param cols: The width of the board in columns.
        """
        self.rows = rows
        self.cols = cols
        self.board = zeros((rows, cols))
        self.slots_filled = 0
        self.p1_win_squares = set()
        self.p2_win_squares = set()

    def print_board(self):
        """
        Prints the state of the board to the console.
        """
        print(flip(self.board, 0))
        print(" ---------------------")
        print(" " + str([1, 2, 3, 4, 5, 6, 7]))

    def drop_piece(self, row, col, piece):
        """
        Drops a piece into the slot at position (row, col)
        :param row: The row of the slot.
        :param col: The column of the slot.
        :param piece: The piece to drop.
        """
        self.board[row][col] = piece
        self.slots_filled += 1

        coord = (row, col)
        if piece == 1:
            if coord in self.p2_win_squares:
                self.p2_win_squares.remove(coord)
        elif piece == 2:
            if coord in self.p1_win_squares:
                self.p1_win_squares.remove(coord)

    def is_valid_location(self, col):
        """
        Returns whether the position exists on the board.
        :param col: The column to check.
        :return: Whether the specified column exists on the board.
        """
        return self.board[self.rows - 1][col] == 0

    def get_next_open_row(self, col):
        """
        Returns the next free row for a column.
        :param col: The column to check for a free space.
        :return: The next free row for a column.
        """
        for row in range(self.rows):
            if self.board[row][col] == 0:
                return row

    def is_valid_coord(self, r, c) -> bool:
        """
        If the space is off of the board it returns False.

        :param r: The row to check.
        :param c: The column to check.
        :return: Whether the square is on the board and has the color/piece specified.
        """
        if r < 0 or r >= self.rows:
            return False

        if c < 0 or c >= self.cols:
            return False

        return True

    def check_square(self, piece, r, c) -> bool:
        """
        Checks if a particular square is a certain color.  If
        the space is off of the board it returns False.

        :param piece: The piece color to look for.
        :param r: The row to check.
        :param c: The column to check.
        :return: Whether the square is on the board and has the color/piece specified.
        """
        if not self.is_valid_coord(r, c):
            return False

        return self.board[r][c] == piece

    def horizontal_win(self, piece, r, c) -> bool:
        """
        Checks if there is a horizontal win at the position (r,c)
        :param piece: The color of the chip to check for.
        :param r: The row.
        :param c: The column.
        :return: Whether there is a horizontal win at the position (r, c).
        """
        consecutive_pieces = 0
        for c in range(c - 3, c + 4):
            if self.check_square(piece, r, c):
                consecutive_pieces += 1
                if consecutive_pieces == 4:
                    return True
            else:
                consecutive_pieces = 0

        return False

    def vertical_win(self, piece, r, c) -> bool:
        """
        Checks if there is vertical win at the position (r, c)
        :param piece: The color of the chip to check for.
        :param r: The row
        :param c: The column
        :return: Whether there is a vertical win at the position (r, c)
        """
        consecutive_pieces = 0
        for r in range(r - 3, r + 1):
            if self.check_square(piece, r, c):
                consecutive_pieces += 1

        return consecutive_pieces == 4

    def diagonal_win(self, piece, r, c):
        """
        Checks if there is a diagonal_win at the position (r, c)
        :param piece: The color of the chip to check for.
        :param r: The row
        :param c: The column
        :return: Whether there is a diagonal win at the position (r,c)
        """
        consecutive_pieces = 0
        for r_1, c_1 in zip(range(r - 3, r + 4), range(c + 3, c - 4, -1)):
            if self.check_square(piece, r_1, c_1):
                consecutive_pieces += 1
                if consecutive_pieces == 4:
                    return True
            else:
                consecutive_pieces = 0

        consecutive_pieces = 0
        for r_2, c_2 in zip(range(r - 3, r + 4), range(c - 3, c + 4)):
            if self.check_square(piece, r_2, c_2):
                consecutive_pieces += 1
                if consecutive_pieces == 4:
                    return True
            else:
                consecutive_pieces = 0

        return False

    def _set_horizontal_win_squares(self, piece, r, c):
        """
        Set the squares where is a horizontal win square surround the position (r, c)
        :param piece: The color of the chip to check for.
        :param r: The row.
        :param c: The column.
        :return: Whether there is a horizontal win at the position (r, c).
        """
        for c in range(c - 3, c + 4):
            self._set_win_square(piece, r, c, "h")

    def _set_vertical_win_squares(self, piece, r, c):
        """
        Set the squares where is a vertical win square surround the position (r, c)
        :param piece: The color of the chip to check for.
        :param r: The row
        :param c: The column
        :return: Whether there is a vertical win at the position (r, c)
        """
        for r in range(r - 3, r + 4):
            self._set_win_square(piece, r, c, "v")

    def _set_diagonal_win_squares(self, piece, r, c):
        """
        Set the squares where is a diagonal win square surround the position (r, c)
        :param piece: The color of the chip to check for.
        :param r: The row
        :param c: The column
        :return: Whether there is a diagonal win at the position (r,c)
        """
        for r_1, c_1 in zip(range(r - 3, r + 4), range(c + 3, c - 4, -1)):
            self._set_win_square(piece, r_1, c_1, "d")

        for r_2, c_2 in zip(range(r - 3, r + 4), range(c - 3, c + 4)):
            self._set_win_square(piece, r_2, c_2, "d")

    def _set_win_square(self, piece, r, c, direction: str):
        """
        Add the coordinates of the winning squares surround
        the given coordinates to the pertinent attribute
        (p1_win_squares or p2_win_squares) if is a winning square
        :param piece: The color of the chip to check for.
        :param r: The row
        :param c: The column
        :param direction: if it is [v]ertical, [d]iagonal or [h]orizontal
        """
        if self.is_valid_coord(r, c):
            if self.board[r][c] == 0:
                self.board[r][c] = piece

                if direction == "v":
                    check = self.vertical_win(piece, r, c)
                elif direction == "d":
                    check = self.diagonal_win(piece, r, c)
                elif direction == "h":
                    check = self.horizontal_win(piece, r, c)
                else:
                    raise ValueError("Parameter 'direction' must be: 'h', 'v' or 'd'")

                if piece == 1 and check:
                    self.p1_win_squares.add((r, c))
                elif piece == 2 and check:
                    self.p2_win_squares.add((r, c))

                self.board[r][c] = 0

    def _analyze_square(self, piece, r, c):
        """
        This function check for all the possible winning squares
        surround the given coordinates and add them to the pertinent attribute
        (p1_win_squares or p2_win_squares)
        :param piece: The color of the chip to check for.
        :param r: The row
        :param c: The column
        """
        self._set_horizontal_win_squares(piece, r, c)
        self._set_vertical_win_squares(piece, r, c)
        self._set_diagonal_win_squares(piece, r, c)

    def winning_move(self, piece, r, c) -> bool:
        """
        Checks if the current piece has won the game.
        :param piece: The color of the chip to check for.
        :param r: The row
        :param c: The column
        :return: Whether the current piece has won the game.
        """
        self._analyze_square(piece, r, c)
        if piece == 1:
            return (r, c) in self.p1_win_squares

        return (r, c) in self.p2_win_squares

    def tie_move(self):
        """
        Checks for a tie game.
        :return:  Whether a tie has occurred.
        """
        return self.slots_filled == (self.rows * self.cols)

    def __str__(self):
        return str(self.board)
