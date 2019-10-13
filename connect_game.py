import math
import sys
from typing import Tuple
from config import black
from game_data import GameData
from graphics import GameRenderer

import pygame

class ConnectGame:
    game_data: GameData
    renderer: GameRenderer

    def __init__(self, game_data: GameData, renderer: GameRenderer):
        self.game_data = game_data
        self.renderer = renderer

        self.sq_size: int = 100

        self.width: int = 7 * self.sq_size
        self.height: int = 7 * self.sq_size
        self.size: Tuple[int, int] = (self.width, self.height)
        self.radius: int = int(self.sq_size / 2 - 5)

    def quit(self):
        sys.exit()

    def mouse_move(self, posx: int):
        # Queue message that mouse has been moved
        # Set the x coordinate
        ### Renderer should see action is mouse move, and draw this ##########################
        pygame.draw.rect(self.renderer.screen, black, (0, 0, self.width, self.sq_size))
        if self.game_data.turn == 0:
            self.renderer.draw_red_coin(posx - (self.sq_size / 2), int(self.sq_size) - self.sq_size + 5)
        else:
            self.renderer.draw_yellow_coin(posx - (self.sq_size / 2), int(self.sq_size) - self.sq_size + 5)
        #######################################################################################

    def mouse_click(self, posx: int):
        # Queue message that the mouse has been clicked
        # Set the x coordinate

        ### Renderer should see action is mouse click, and draw this ##########################
        pygame.draw.rect(self.renderer.screen, black, (0, 0, self.width, self.sq_size))
        #######################################################################################
        if self.game_data.turn == 0:

            col: int = int(math.floor(posx / self.sq_size))

            if self.game_data.game_board.is_valid_location(col):
                row: int = self.game_data.game_board.get_next_open_row( col)

                self.game_data.last_move_row = row
                self.game_data.last_move_col = col
                self.game_data.game_board.drop_piece(row, col, 1)

            self.print_board()

            if self.game_data.game_board.winning_move(1):
                self.game_data.action ="player_1_wins"
                self.game_data.game_over = True
        else:
            col: int = int(math.floor(posx / self.sq_size))

            if self.game_data.game_board.is_valid_location(col):
                row: int = self.game_data.game_board.get_next_open_row( col)

                self.game_data.last_move_row = row
                self.game_data.last_move_col = col
                self.game_data.game_board.drop_piece( row, col, 2)

            self.print_board()

            if self.game_data.game_board.winning_move( 2):
                self.game_data.action = "player_2_wins"
                self.game_data.game_over = True

        pygame.display.update()
        self.game_data.turn += 1
        self.game_data.turn = self.game_data.turn % 2

    def undo(self):
        self.game_data.game_board.drop_piece(
            self.game_data.last_move_row,
            self.game_data.last_move_col,
            0
        )

        self.game_data.action = "undo"

        self.game_data.turn += 1
        self.game_data.turn = self.game_data.turn % 2

    def update(self):
        if self.game_data.game_board.tie_move():
            self.game_data.action = "tie"
            self.game_data.game_over = True

        if self.game_data.game_over:
            pass
            # print(os.getpid())
            #pygame.time.wait(3000)
            #os.system("kill " + str(os.getpid()))
            #os.system("./restart.sh")

    def draw(self):
        self.renderer.draw(self.game_data)

    def print_board(self):
        self.game_data.game_board.print_board()
