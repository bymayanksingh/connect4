
from numpy import flip, zeros

class GameBoard:
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

class GameData:
    def __init__(self):
        self.coin_position = 0
        self.game_over = False
        self.turn = 0
        self.last_move_row = 0
        self.last_move_col = 0
        self.game_board = GameBoard()
