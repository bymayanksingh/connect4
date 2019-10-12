
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

    def __init__(self,rows =6, cols=7):
        self.rows = rows
        self.cols = cols
        self.board = zeros((rows, cols))

    def print_board(self):
        print(flip(self.board, 0))
        print(" ---------------------")
        print(" " + str([1, 2, 3, 4, 5, 6, 7]))

    def drop_piece(self, row, col, piece):
        self.board[row][col] = piece

    def is_valid_location(self, col):
        return self.board[self.rows - 1][col] == 0

    def get_next_open_row(self, col):
        for row in range(self.rows):
            if self.board[row][col] == 0:
                return row

    def winning_move(self, piece):
        for c in range(self.cols - 3):
            for r in range(self.rows):
                if (
                        self.board[r][c] == piece
                        and self.board[r][c + 1] == piece
                        and self.board[r][c + 2] == piece
                        and self.board[r][c + 3] == piece
                ):
                    return True

        for c in range(self.cols):
            for r in range(self.rows - 3):
                if (
                        self.board[r][c] == piece
                        and self.board[r + 1][c] == piece
                        and self.board[r + 2][c] == piece
                        and self.board[r + 3][c] == piece
                ):
                    return True

        for c in range(self.cols - 3):
            for r in range(self.rows - 3):
                if (
                        self.board[r][c] == piece
                        and self.board[r + 1][c + 1] == piece
                        and self.board[r + 2][c + 2] == piece
                        and self.board[r + 3][c + 3] == piece
                ):
                    return True

        for c in range(self.cols - 3):
            for r in range(3, self.rows):
                if (
                        self.board[r][c] == piece
                        and self.board[r - 1][c + 1] == piece
                        and self.board[r - 2][c + 2] == piece
                        and self.board[r - 3][c + 3] == piece
                ):
                    return True

    def tie_move(self):
        slots_filled: int = 0

        for c in range(self.cols):
            for r in range(self.rows):
                if self.board[r][c] != 0:
                    slots_filled += 1

        return slots_filled == 42


class GameData:
    """
    The game data class contains all of the data for the game.
    """
    game_over: bool
    turn: int
    last_move_row: int
    last_move_col: int
    game_board: GameBoard

    def __init__(self):
        self.game_over = False
        self.turn = 0
        self.last_move_row = 0
        self.last_move_col = 0
        self.game_board = GameBoard()
