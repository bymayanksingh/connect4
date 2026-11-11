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
    win_condition: int  # Number of pieces needed in a row to win

    def __init__(self, rows=6, cols=7, win_condition=4):
        """
        Initializes the game board.
        :param rows: The height of the board in rows.
        :param cols: The width of the board in columns.
        :param win_condition: Number of pieces needed in a row to win.
        """
        self.rows = rows
        self.cols = cols
        self.win_condition = win_condition
        self.board = zeros((rows, cols))

    def print_board(self):
        """
        Prints the state of the board to the console.
        """
        print(flip(self.board, 0))
        # Adjust column numbers display based on number of columns
        col_nums = [i+1 for i in range(self.cols)]
        col_display = " " + str(col_nums)
        separator = " " + "-" * (self.cols * 2 + 1)
        print(separator)
        print(col_display)

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
        Returns whether the position exists on the board and is a valid drop location.
        :param col: The column to check.
        :return: Whether the specified column exists and is not full.
        """
        # First check if column is in bounds
        if col < 0 or col >= self.cols:
            return False
        # Then check if the top spot is empty
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
        # Check if there's enough space to the right for a win
        if c + self.win_condition > self.cols:
            return False
            
        # Check if all positions contain the piece
        for i in range(self.win_condition):
            if not self.check_square(piece, r, c + i):
                return False
                
        return True

    def vertical_win(self, piece, r, c):
        """
        Checks if there is vertical win at the position (r, c)
        :param piece: The color of the chip to check for.
        :param r: The row
        :param c: The column
        :return: Whether there is a vertical win at the position (r, c)
        """
        # Check if there's enough space above for a win
        if r + self.win_condition > self.rows:
            return False
            
        # Check if all positions contain the piece
        for i in range(self.win_condition):
            if not self.check_square(piece, r + i, c):
                return False
                
        return True

    def diagonal_win(self, piece, r, c):
        """
        Checks if there is a diagonal_win at the position (r, c)
        :param piece: The color of the chip to check for.
        :param r: The row
        :param c: The column
        :return: Whether there is a diagonal win at the position (r,c)
        """
        # Check positive diagonal (/)
        if r + self.win_condition <= self.rows and c + self.win_condition <= self.cols:
            for i in range(self.win_condition):
                if not self.check_square(piece, r + i, c + i):
                    break
            else:
                return True
                
        # Check negative diagonal (\)
        if r >= self.win_condition - 1 and c + self.win_condition <= self.cols:
            for i in range(self.win_condition):
                if not self.check_square(piece, r - i, c + i):
                    break
            else:
                return True
                
        return False

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
        total_slots = self.rows * self.cols

        for c in range(self.cols):
            for r in range(self.rows):
                if self.board[r][c] != 0:
                    slots_filled += 1

        return slots_filled == total_slots
