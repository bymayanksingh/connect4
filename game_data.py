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
    title_height: int
    sq_size: int
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
        self.game_board = GameBoard(10,20) #Change the size of the board here
        self.action = None

        SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size() #Resolution of the screen

        self.height: int = (SCREEN_HEIGHT*7)//10
        self.width: int = (SCREEN_WIDTH*8)//10
        self.sq_size: int = min(self.height//(self.game_board.rows), self.width//(self.game_board.cols), 100)
        self.margin: int = self.sq_size//20
        self.title_height = SCREEN_HEIGHT//20
        self.height: int = self.sq_size * (self.game_board.rows) + self.title_height + 2*self.margin + self.sq_size
        self.width: int = self.sq_size * self.game_board.cols
        self.size: Tuple[int, int] = (self.width, self.height)
        self.radius: int = int(self.sq_size / 2 - self.margin)
