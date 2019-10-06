
from numpy import flip, zeros

class GameBoard:
    def __init__(self,rows =6, cols=7):
        self.board = zeros((rows, cols))

class GameData:
    def __init__(self):
        self.coin_position = 0
        self.game_over = False
        self.turn = 0
        self.last_move_row = 0
        self.last_move_col = 0
        self.game_board = GameBoard()
