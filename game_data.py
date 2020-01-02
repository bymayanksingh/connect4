from typing import Tuple

from assets import (black_coin, disc_drop_1, disc_drop_2, event_sound,
                    red_coin, yellow_coin)
from config import black, blue, green, red, violet, white, yellow
from game_board import GameBoard


class GameData:
    """
    The game data class contains all of the data for the game.
    """

    radius: int
    height: int
    width: int
    sq_size: int
    size: Tuple[int, int]
    game_over: bool
    turn: int
    last_move_row: [int]
    last_move_col: [int]
    game_board: GameBoard

    def __init__(self, color_player1=red, color_player2=yellow ,back_color=blue):
        self.game_over = False
        self.turn = 0
        self.last_move_row = []
        self.last_move_col = []
        self.game_board = GameBoard()
        self.action = None
        self.c1 = color_player1
        self.c2 = color_player2
        self.bg = back_color
        self.sq_size: int = 100
        self.width: int = 7 * self.sq_size
        self.height: int = 7 * self.sq_size
        self.size: Tuple[int, int] = (self.width, self.height)
        self.radius: int = int(self.sq_size / 2 - 5)
