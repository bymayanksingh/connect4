import math
import os
import sys

import pygame

from pygame import mixer
from pygame.gfxdraw import aacircle, filled_circle
from pygame.locals import KEYDOWN

from assets import *
from config import *
from game_data import GameData
from graphics import GameRenderer

rows = 6
cols = 7
sq_size = 100
width = cols * sq_size
height = (rows + 1) * sq_size
size = (width, height)
radius = int(sq_size / 2 - 5)

pygame.init()
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Connect Four | Mayank Singh")
myfont = pygame.font.SysFont("monospace", 75)
label = myfont.render("CONNECT FOUR!!", 1, white)

game_data = GameData()
renderer = GameRenderer(screen)

screen.blit(label, (40, 10))
pygame.display.update()


def undo_move(board, row, col):
    game_data.game_board.drop_piece(row, col, 0)
    filled_circle(screen, int(row), int(col), radius, black)
    aacircle(screen, int(row), int(col), radius, black)
    renderer.draw_black_coin(int(col * sq_size) + 5, height - int(row * sq_size + sq_size - 5))
    board.print_board()


game_data.game_board.print_board()
renderer.draw_board(game_data.game_board)
pygame.display.update()
pygame.time.wait(1000)

while not game_data.game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, black, (0, 0, width, sq_size))
            posx = event.pos[0]
            if game_data.turn == 0:
                renderer.draw_red_coin(posx - (sq_size / 2), int(sq_size) - sq_size + 5)
            else:
                renderer.draw_yellow_coin(posx - (sq_size / 2), int(sq_size) - sq_size + 5)
        pygame.display.update()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, black, (0, 0, width, sq_size))
            if game_data.turn == 0:
                posx = event.pos[0]
                col = int(math.floor(posx / sq_size))
                if game_data.game_board.is_valid_location(col):
                    row = game_data.game_board.get_next_open_row( col)
                    game_data.last_move_row = row
                    game_data.last_move_col = col
                    game_data.game_board.drop_piece( row, col, 1)
                game_data.game_board.print_board()

                if game_data.game_board.winning_move( 1):
                    label = myfont.render("PLAYER 1 WINS!", 1, red)
                    screen.blit(label, (40, 10))
                    mixer.music.load(event_sound)
                    mixer.music.play(0)
                    game_data.game_over = True
                pygame.display.update()
            else:
                posx = event.pos[0]
                col = int(math.floor(posx / sq_size))
                if game_data.game_board.is_valid_location(col):
                    row = game_data.game_board.get_next_open_row( col)
                    game_data.last_move_row = row
                    game_data.last_move_col = col
                    game_data.game_board.drop_piece( row, col, 2)
                game_data.game_board.print_board()

                if game_data.game_board.winning_move( 2):
                    label = myfont.render("PLAYER 2 WINS!", 1, yellow)
                    screen.blit(label, (40, 10))
                    mixer.music.load(event_sound)
                    mixer.music.play(0)
                    game_data.game_over = True
                pygame.display.update()
            game_data.turn += 1
            game_data.turn = game_data.turn % 2

        if event.type == KEYDOWN:
            if event.key == pygame.K_z:
                mods = pygame.key.get_mods()
                if mods & pygame.KMOD_CTRL:
                    undo_move(game_data.game_board.board, game_data.last_move_row, game_data.last_move_col)
                    game_data.turn += 1
                    game_data.turn = game_data.turn % 2
        # tie
        if game_data.game_board.tie_move():
            mixer.music.load(os.path.join("sounds", "event.ogg"))
            mixer.music.play(0)
            game_data.game_over = True

            myfont = pygame.font.SysFont("monospace", 75)
            label = myfont.render("GAME DRAW !!!!", 1, white)
            screen.blit(label, (40, 10))
            pygame.display.update()

        if game_data.game_over:
            # print(os.getpid())
            pygame.time.wait(3000)
            #os.system("kill " + str(os.getpid()))
            #os.system("./restart.sh")
        renderer.draw_board(game_data.game_board)