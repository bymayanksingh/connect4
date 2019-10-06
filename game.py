import math
import os
import sys

import pygame
from numpy import flip, zeros
from pygame import mixer
from pygame.gfxdraw import aacircle, filled_circle
from pygame.locals import KEYDOWN

from assets import *
from config import *
from game_data import GameData

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


screen.blit(label, (40, 10))
pygame.display.update()


def draw_black_coin(x, y):
    screen.blit(black_coin, (x, y))


def draw_red_coin(x, y):
    screen.blit(red_coin, (x, y))


def draw_yellow_coin(x, y):
    screen.blit(yellow_coin, (x, y))


















def tie_move():
    slots_filled = 0
    for c in range(cols):
        for r in range(rows):
            if game_data.game_board.board[r][c] != 0:
                slots_filled += 1

    if slots_filled == 42:
        myfont = pygame.font.SysFont("monospace", 75)
        label = myfont.render("GAME DRAW !!!!", 1, white)
        screen.blit(label, (40, 10))
        pygame.display.update()
        return True


def undo_move(board, row, col):
    game_data.game_board.drop_piece(row, col, 0)
    filled_circle(screen, int(row), int(col), radius, black)
    aacircle(screen, int(row), int(col), radius, black)
    draw_black_coin(int(col * sq_size) + 5, height - int(row * sq_size + sq_size - 5))
    board.print_board()


def draw_board(board):
    for c in range(cols):
        for r in range(rows):
            pygame.draw.rect(
                screen, blue, (c * sq_size, (r + 1) * sq_size, sq_size, sq_size)
            )
            aacircle(
                screen,
                int(c * sq_size + sq_size / 2),
                int((r + 1) * sq_size + sq_size / 2),
                radius,
                black,
            )
            filled_circle(
                screen,
                int(c * sq_size + sq_size / 2),
                int((r + 1) * sq_size + sq_size / 2),
                radius,
                black,
            )
            # pygame.draw.circle(screen, black, (int(c*sq_size + sq_size/2), int((r+1) * sq_size + sq_size/2)), radius)

    for c in range(cols):
        for r in range(rows):
            if board[r][c] == 1:
                draw_red_coin(
                    int(c * sq_size) + 5, height - int(r * sq_size + sq_size - 5)
                )
                mixer.music.load(disc_drop_1)
                mixer.music.play(0)
            elif board[r][c] == 2:
                draw_yellow_coin(
                    int(c * sq_size) + 5, height - int(r * sq_size + sq_size - 5)
                )
                mixer.music.load(disc_drop_2)
                mixer.music.play(0)
    pygame.display.update()

game_data.game_board.print_board()
draw_board(game_data.game_board.board)
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
                draw_red_coin(posx - (sq_size / 2), int(sq_size) - sq_size + 5)
            else:
                draw_yellow_coin(posx - (sq_size / 2), int(sq_size) - sq_size + 5)
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
                draw_board(game_data.game_board.board)
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
                draw_board(game_data.game_board.board)
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
        if tie_move():
            mixer.music.load("event.ogg")
            mixer.music.play(0)
            game_data.game_over = True

        if game_data.game_over:
            # print(os.getpid())
            pygame.time.wait(3000)
            os.system("kill " + str(os.getpid()))
            os.system("./restart.sh")
