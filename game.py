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
from game_data import GameData, GameBoard
from graphics import GameRenderer

rows: int = 6
cols: int = 7
sq_size: int = 100
width: int = cols * sq_size
height: int = (rows + 1) * sq_size
size: Tuple[int, int] = (width, height)
radius: int = int(sq_size / 2 - 5)

pygame.init()
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Connect Four | Mayank Singh")

myfont = pygame.font.SysFont("monospace", 75)
label = myfont.render("CONNECT FOUR!!", 1, white)

screen.blit(label, (40, 10))
pygame.display.update()

class ConnectGame:
    def __init__(self, game_data, renderer):
        self.game_data = game_data
        self.renderer = renderer

    def quit(self):
        sys.exit()

    def mouse_move(self, posx):
        pygame.draw.rect(screen, black, (0, 0, width, sq_size))

        if self.game_data.turn == 0:
            self.renderer.draw_red_coin(posx - (sq_size / 2), int(sq_size) - sq_size + 5)
        else:
            self.renderer.draw_yellow_coin(posx - (sq_size / 2), int(sq_size) - sq_size + 5)

    def mouse_click(self, posx):
        pygame.draw.rect(screen, black, (0, 0, width, sq_size))
        if self.game_data.turn == 0:

            col: int = int(math.floor(posx / sq_size))

            if self.game_data.game_board.is_valid_location(col):
                row: int = self.game_data.game_board.get_next_open_row( col)

                self.game_data.last_move_row = row
                self.game_data.last_move_col = col
                self.game_data.game_board.drop_piece(row, col, 1)

            self.game_data.game_board.print_board()

            if self.game_data.game_board.winning_move(1):
                label = myfont.render("PLAYER 1 WINS!", 1, red)
                screen.blit(label, (40, 10))
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

            self.game_data.game_board.print_board()

            if self.game_data.game_board.winning_move( 2):
                label = myfont.render("PLAYER 2 WINS!", 1, yellow)
                screen.blit(label, (40, 10))
                mixer.music.load(event_sound)
                mixer.music.play(0)
                self.game_data.game_over = True
            pygame.display.update()
        self.game_data.turn += 1
        self.game_data.turn = self.game_data.turn % 2

    def undo_move(self, row: int, col: int):
        self.game_data.game_board.drop_piece(row, col, 0)
        filled_circle(screen, int(row), int(col), radius, black)
        aacircle(screen, int(row), int(col), radius, black)
        self.renderer.draw_black_coin(int(col * sq_size) + 5, height - int(row * sq_size + sq_size - 5))
        self.game_data.game_board.print_board()

    def undo(self):
        self.undo_move(self.game_data.last_move_row, self.game_data.last_move_col)
        self.game_data.turn += 1
        self.game_data.turn = self.game_data.turn % 2
    def update(self):
        pass
    def draw(self):
        self.renderer.draw(game.game_data)


game = ConnectGame(GameData(), GameRenderer(screen))

game.game_data.game_board.print_board()
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