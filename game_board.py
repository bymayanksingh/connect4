from numpy import flip, zeros
from numpy.core._multiarray_umath import ndarray


class GameBoard:
    """
    The GameBoard class holds the state of the game board,
    and methods to manipulate and query the board.
    """

    board: ndarray
    cols: int
    rows: int

    def __init__(self, rows=6, cols=7):
        """
        Initializes the game board.
        :param rows: The height of the board in rows.
        :param cols: The width of the boarrd in columns.
        """
        self.rows = rows
        self.cols = cols
        self.board = zeros((rows, cols))

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

    def check_square(self, piece, r, c):
        """
        Checks if a particular square is a certain color.  If
        the space is off of the board it returns False.

        :param piece: The piece color to look for.
        :param r: The row to check.
        :param c: The column to check.
        :return: Whether the square is on the board and has the color/piece specified.
        """
        if r < 0 or r >= self.rows:
            return False

        if c < 0 or c >= self.cols:
            return False

        return self.board[r][c] == piece

    def horizontal_win(self, piece, r, c):
        """
        Checks if there is a horizontal win at the position (r,c)
        :param piece: The color of the chip to check for.
        :param r: The row.
        :param c: The column.
        :return: Whether there is a horizontal win at the position (r, c).
        """
        return (
            self.check_square(piece, r, c)
            and self.check_square(piece, r, c + 1)
            and self.check_square(piece, r, c + 2)
            and self.check_square(piece, r, c + 3)
        )

    def vertical_win(self, piece, r, c):
        """
        Checks if there is vertical win at the position (r, c)
        :param piece: The color of the chip to check for.
        :param r: The row
        :param c: The column
        :return: Whether there is a vertical win at the position (r, c)
        """
        return (
            self.check_square(piece, r, c)
            and self.check_square(piece, r + 1, c)
            and self.check_square(piece, r + 2, c)
            and self.check_square(piece, r + 3, c)
        )

    def diagonal_win(self, piece, r, c):
        """
        Checks if there is a diagonal_win at the position (r, c)
        :param piece: The color of the chip to check for.
        :param r: The row
        :param c: The column
        :return: Whether there is a diagonal win at the position (r,c)
        """
        return (
            self.check_square(piece, r, c)
            and self.check_square(piece, r + 1, c + 1)
            and self.check_square(piece, r + 2, c + 2)
            and self.check_square(piece, r + 3, c + 3)
        ) or (
            self.check_square(piece, r, c)
            and self.check_square(piece, r - 1, c + 1)
            and self.check_square(piece, r - 2, c + 2)
            and self.check_square(piece, r - 3, c + 3)
        )

    def winning_move(self, piece):
        """
        Checks if the current piece has won the game.
        :param piece: The color of the chip to check for.
        :return: Whether the current piece has won the game.
        """
        for c in range(self.cols):
            for r in range(self.rows):
                if (
                    self.horizontal_win(piece, r, c)
                    or self.vertical_win(piece, r, c)
                    or self.diagonal_win(piece, r, c)
                ):
                    return True
        return False

    def tie_move(self):
        """
        Checks for a tie game.
        :return:  Whether a tie has occurred.
        """
        slots_filled: int = 0

        for c in range(self.cols):
            for r in range(self.rows):
                if self.board[r][c] != 0:
                    slots_filled += 1

        return slots_filled == 42
