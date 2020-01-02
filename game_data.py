from typing import Tuple

from game_board import GameBoard
import pyautogui #For getting screen size


class GameData:
    """
    The game data class contains all of the data for the game.
    """

    radius: int
    height: int
    width: int
    sq_size: int
    font_size: int
    character_width: int
    margin: int
    size: Tuple[int, int]
    game_over: bool
    posx: int
    turn: int
    last_move_row: [int]
    last_move_col: [int]
    game_board: GameBoard

    def __init__(self):
        self.game_over = False
        self.turn = 0
        self.last_move_row = []
        self.last_move_col = []
        self.game_board = GameBoard()
        self.action = None

        SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size() #Resolution of the screen

        self.height: int = (SCREEN_HEIGHT*7)//10
        self.width: int = (SCREEN_WIDTH*8)//10
        self.sq_size: int = min(self.height//(self.game_board.rows), self.width//(self.game_board.cols), 100)
        self.font_size = int(self.sq_size*0.8)
        self.character_width = self.font_size*3//5
        self.margin: int = self.sq_size//20
        self.height: int = self.sq_size * (self.game_board.rows) + self.sq_size
        self.width: int = self.sq_size * self.game_board.cols
        self.size: Tuple[int, int] = (self.width, self.height)
        self.radius: int = int(self.sq_size / 2 - self.margin)
