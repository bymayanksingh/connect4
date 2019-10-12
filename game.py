import math
import os
import sys
from typing import Tuple

import pygame

from pygame import mixer
from pygame.gfxdraw import aacircle, filled_circle
from pygame.locals import KEYDOWN

from assets import *
from config import *
from config import black
from game_data import GameData
from graphics import GameRenderer

sq_size: int = 100

width: int = 7 * sq_size
height: int = 7 * sq_size
size: Tuple[int, int] = (width, height)
radius: int = int(sq_size / 2 - 5)

pygame.init()
screen = pygame.display.set_mode(size)

### Myfont and label need to be moved to the renderer class. ###
pygame.display.set_caption("Connect Four | Mayank Singh")
myfont = pygame.font.SysFont("monospace", 75)
label = myfont.render("CONNECT FOUR!!", 1, white)

screen.blit(label, (40, 10))
################################################################
pygame.display.update()

class ConnectGame:
    game_data: GameData
    renderer: GameRenderer

    def __init__(self, game_data: GameData, renderer: GameRenderer):
        self.game_data = game_data
        self.renderer = renderer

    def quit(self):
        sys.exit()

    def mouse_move(self, posx: int):
        # Queue message that mouse has been moved

        ### Renderer should see action is mouse move, and draw this ##########################
        pygame.draw.rect(self.renderer.screen, black, (0, 0, width, sq_size))
        if self.game_data.turn == 0:
            self.renderer.draw_red_coin(posx - (sq_size / 2), int(sq_size) - sq_size + 5)
        else:
            self.renderer.draw_yellow_coin(posx - (sq_size / 2), int(sq_size) - sq_size + 5)
        #######################################################################################
    def mouse_click(self, posx: int):
        ### Renderer should see action is mouse click, and draw this ##########################
        pygame.draw.rect(self.renderer.screen, black, (0, 0, width, sq_size))
        #######################################################################################
        if self.game_data.turn == 0:

            col: int = int(math.floor(posx / sq_size))

            if self.game_data.game_board.is_valid_location(col):
                row: int = self.game_data.game_board.get_next_open_row( col)

                self.game_data.last_move_row = row
                self.game_data.last_move_col = col
                self.game_data.game_board.drop_piece(row, col, 1)

            self.print_board()

            if self.game_data.game_board.winning_move(1):
                ### Move to renderer #########################
                label = myfont.render("PLAYER 1 WINS!", 1, red)
                self.renderer.screen.blit(label, (40, 10))
                ###############################################

                mixer.music.load(event_sound)
                mixer.music.play(0)
                self.game_data.game_over = True
            pygame.display.update()
        else:
            col: int = int(math.floor(posx / sq_size))

            if self.game_data.game_board.is_valid_location(col):
                row: int = self.game_data.game_board.get_next_open_row( col)

                self.game_data.last_move_row = row
                self.game_data.last_move_col = col
                self.game_data.game_board.drop_piece( row, col, 2)

            self.print_board()

            if self.game_data.game_board.winning_move( 2):
                ##### Move to renderer ###
                label = myfont.render("PLAYER 2 WINS!", 1, yellow)
                screen.blit(label, (40, 10))
                ##########################

                mixer.music.load(event_sound)
                mixer.music.play(0)
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

        ################## Move to Renderer #######################
        filled_circle(
            screen,
            self.game_data.last_move_row,
            self.game_data.last_move_col,
            radius,
            black
        )

        aacircle(
            screen,
            self.game_data.last_move_row,
            self.game_data.last_move_col,
            radius,
            black
        )

        self.renderer.draw_black_coin(
            self.game_data.last_move_col * sq_size + 5,
            height - (self.game_data.last_move_row * sq_size + sq_size - 5)
        )

        self.print_board()
        ############################################################
        self.game_data.turn += 1
        self.game_data.turn = self.game_data.turn % 2

    def update(self):
        pass

    def draw(self):
        self.renderer.draw(game.game_data)

    def print_board(self):
        self.game_data.game_board.print_board()


game = ConnectGame(GameData(), GameRenderer(screen))

game.print_board()
game.draw()

pygame.display.update()
pygame.time.wait(1000)

while not game.game_data.game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.quit()

        if event.type == pygame.MOUSEMOTION:
            game.mouse_move(event.pos[0])

        pygame.display.update()
        if event.type == pygame.MOUSEBUTTONDOWN:
            game.mouse_click(event.pos[0])

        if event.type == KEYDOWN:
            if event.key == pygame.K_z:
                mods: int = pygame.key.get_mods()
                if mods & pygame.KMOD_CTRL:
                    game.undo()
        # tie
        if game.game_data.game_board.tie_move():
            mixer.music.load(os.path.join("sounds", "event.ogg"))
            mixer.music.play(0)
            game.game_data.game_over = True

            myfont = pygame.font.SysFont("monospace", 75)
            label = myfont.render("GAME DRAW !!!!", 1, white)
            screen.blit(label, (40, 10))
            pygame.display.update()

        if game.game_data.game_over:
            # print(os.getpid())
            pygame.time.wait(3000)
            #os.system("kill " + str(os.getpid()))
            #os.system("./restart.sh")

        game.draw()