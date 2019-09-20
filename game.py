import os
import sys
import math
import pygame
from config import *
from assets import *
from numpy import flip
from numpy import zeros
from pygame import mixer
from pygame.locals import KEYDOWN
from pygame.gfxdraw import aacircle
from pygame.gfxdraw import filled_circle

rows = 6
cols = 7
sq_size = 100
game_over = False
turn = 0
width = cols * sq_size
height = (rows + 1) * sq_size
size = (width, height)
radius = int(sq_size / 2 - 5)
last_move_row = 0
last_move_col = 0

pygame.init()
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Connect Four | Mayank Singh")
myfont = pygame.font.SysFont("monospace", 75)
label = myfont.render("CONNECT FOUR!!", 1, white)
screen.blit(label, (40, 10))
pygame.display.update()


def draw_black_coin(x, y):
    screen.blit(black_coin, (x, y))


def draw_red_coin(x, y):
    screen.blit(red_coin, (x, y))


def draw_yellow_coin(x, y):
    screen.blit(yellow_coin, (x, y))


def init_board():
    board = zeros((rows, cols))
    return board


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col):
    return board[rows - 1][col] == 0


def get_next_open_row(board, col):
    for row in range(rows):
        if board[row][col] == 0:
            return row


def print_board(board):
    print(flip(board, 0))
    print(" ---------------------")
    print(" " + str([1, 2, 3, 4, 5, 6, 7]))


def winning_move(board, piece):
    for c in range(cols - 3):
        for r in range(rows):
            if (
                board[r][c] == piece
                and board[r][c + 1] == piece
                and board[r][c + 2] == piece
                and board[r][c + 3] == piece
            ):
                return True

    for c in range(cols):
        for r in range(rows - 3):
            if (
                board[r][c] == piece
                and board[r + 1][c] == piece
                and board[r + 2][c] == piece
                and board[r + 3][c] == piece
            ):
                return True

    for c in range(cols - 3):
        for r in range(rows - 3):
            if (
                board[r][c] == piece
                and board[r + 1][c + 1] == piece
                and board[r + 2][c + 2] == piece
                and board[r + 3][c + 3] == piece
            ):
                return True

    for c in range(cols - 3):
        for r in range(3, rows):
            if (
                board[r][c] == piece
                and board[r - 1][c + 1] == piece
                and board[r - 2][c + 2] == piece
                and board[r - 3][c + 3] == piece
            ):
                return True


def tie_move():
    slots_filled = 0
    for c in range(cols):
        for r in range(rows):
            if board[r][c] != 0:
                slots_filled += 1

    if slots_filled == 42:
        myfont = pygame.font.SysFont("monospace", 75)
        label = myfont.render("GAME DRAW !!!!", 1, white)
        screen.blit(label, (40, 10))
        pygame.display.update()
        return True


def undo_move(board, row, col):
    drop_piece(board, row, col, 0)
    filled_circle(screen, int(row), int(col), radius, black)
    aacircle(screen, int(row), int(col), radius, black)
    draw_black_coin(int(col * sq_size) + 5, height - int(row * sq_size + sq_size - 5))
    print_board(board)


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


board = init_board()
print_board(board)
draw_board(board)
pygame.display.update()
pygame.time.wait(1000)

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, black, (0, 0, width, sq_size))
            posx = event.pos[0]
            if turn == 0:
                draw_red_coin(posx - (sq_size / 2), int(sq_size) - sq_size + 5)
            else:
                draw_yellow_coin(posx - (sq_size / 2), int(sq_size) - sq_size + 5)
        pygame.display.update()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, black, (0, 0, width, sq_size))
            if turn == 0:
                posx = event.pos[0]
                col = int(math.floor(posx / sq_size))
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    last_move_row = row
                    last_move_col = col
                    drop_piece(board, row, col, 1)
                print_board(board)
                draw_board(board)
                if winning_move(board, 1):
                    label = myfont.render("PLAYER 1 WINS!", 1, red)
                    screen.blit(label, (40, 10))
                    mixer.music.load(event_sound)
                    mixer.music.play(0)
                    game_over = True
                pygame.display.update()
            else:
                posx = event.pos[0]
                col = int(math.floor(posx / sq_size))
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    last_move_row = row
                    last_move_col = col
                    drop_piece(board, row, col, 2)
                print_board(board)
                draw_board(board)
                if winning_move(board, 2):
                    label = myfont.render("PLAYER 2 WINS!", 1, yellow)
                    screen.blit(label, (40, 10))
                    mixer.music.load(event_sound)
                    mixer.music.play(0)
                    game_over = True
                pygame.display.update()
            turn += 1
            turn = turn % 2

        if event.type == KEYDOWN:
            if event.key == pygame.K_z:
                mods = pygame.key.get_mods()
                if mods & pygame.KMOD_CTRL:
                    undo_move(board, last_move_row, last_move_col)
                    turn += 1
                    turn = turn % 2
        # tie
        if tie_move():
            mixer.music.load("event.ogg")
            mixer.music.play(0)
            game_over = True

        if game_over:
            # print(os.getpid())
            pygame.time.wait(3000)
            os.system("kill " + str(os.getpid()))
            os.system("./restart.sh")
