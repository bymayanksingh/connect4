import os
import sys
import math
import pygame
import numpy as np
import pygame.locals
import pygame.gfxdraw
from pygame import mixer

rows = 6
cols = 7
squaresize = 100
game_over = False
turn = 0
width = cols * squaresize
height = (rows + 1) * squaresize
size = (width, height)
yellow = (255, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
black = (0, 0, 0)
radius = int(squaresize / 2 - 5)
last_move_row = 0
last_move_col = 0

pygame.init()
pygame.display.set_caption("Connect4")

redCoinImg = pygame.image.load("redball90px.png")
yellowCoinImg = pygame.image.load("yellowball90px.png")
blackCoinImg = pygame.image.load("blackball91px.png")


def blackcoin(x, y):
    screen.blit(blackCoinImg, (x, y))


def redcoin(x, y):
    screen.blit(redCoinImg, (x, y))


def yellowcoin(x, y):
    screen.blit(yellowCoinImg, (x, y))


def create_board():
    board = np.zeros((rows, cols))
    return board


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col):
    return board[rows - 1][col] == 0


def get_next_open_row(board, col):
    for r in range(rows):
        if board[r][col] == 0:
            return r


def print_board(board):
    print(np.flipr(board, 0))
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
    slotsfilled = 0
    for c in range(cols):
        for r in range(rows):
            if board[r][c] != 0:
                slotsfilled += 1

    if slotsfilled == 42:
        myfont = pygame.font.SysFont("monospace", 75)
        label = myfont.render("GAME DRAW !!!!", 1, white)
        screen.blit(label, (40, 10))
        pygame.display.update()
        return True


def undo_move(board, row, col):
    drop_piece(board, row, col, 0)
    pygame.gfxdraw.filled_circle(screen, int(row), int(col), radius, black)
    pygame.gfxdraw.aacircle(screen, int(row), int(col), radius, black)
    blackcoin(
        int(col * squaresize) + 5, height - int(row * squaresize + squaresize - 5)
    )
    print_board(board)


def draw_board(board):
    for c in range(cols):
        for r in range(rows):
            pygame.draw.rect(
                screen,
                blue,
                (c * squaresize, (r + 1) * squaresize, squaresize, squaresize),
            )
            pygame.gfxdraw.aacircle(
                screen,
                int(c * squaresize + squaresize / 2),
                int((r + 1) * squaresize + squaresize / 2),
                radius,
                black,
            )
            pygame.gfxdraw.filled_circle(
                screen,
                int(c * squaresize + squaresize / 2),
                int((r + 1) * squaresize + squaresize / 2),
                radius,
                black,
            )
            # pygame.draw.circle(screen, black, (int(c*squaresize + squaresize/2), int((r+1) * squaresize + squaresize/2)), radius)

    for c in range(cols):
        for r in range(rows):
            if board[r][c] == 1:
                redcoin(
                    int(c * squaresize) + 5,
                    height - int(r * squaresize + squaresize - 5),
                )
                pygame.mixer.music.load("disc_drop1.wav")
                pygame.mixer.music.play(0)
            elif board[r][c] == 2:
                yellowcoin(
                    int(c * squaresize) + 5,
                    height - int(r * squaresize + squaresize - 5),
                )
                pygame.mixer.music.load("disc_drop2.wav")
                pygame.mixer.music.play(0)
    pygame.display.update()


board = create_board()
print_board(board)
screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()
myfont = pygame.font.SysFont("monospace", 75)
label = myfont.render("CONNECT FOUR!!", 1, white)
screen.blit(label, (40, 10))
pygame.display.update()
pygame.time.wait(1000)

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, black, (0, 0, width, squaresize))
            posx = event.pos[0]
            if turn == 0:
                redcoin(posx - (squaresize / 2), int(squaresize) - squaresize + 5)
            else:
                yellowcoin(posx - (squaresize / 2), int(squaresize) - squaresize + 5)
        pygame.display.update()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, black, (0, 0, width, squaresize))
            if turn == 0:
                posx = event.pos[0]
                col = int(math.floor(posx / squaresize))
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
                    pygame.mixer.music.load("event.ogg")
                    pygame.mixer.music.play(0)
                    game_over = True
                pygame.display.update()
            else:
                posx = event.pos[0]
                col = int(math.floor(posx / squaresize))
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
                    pygame.mixer.music.load("event.ogg")
                    pygame.mixer.music.play(0)
                    game_over = True
                pygame.display.update()
            turn += 1
            turn = turn % 2

        if event.type == pygame.locals.KEYDOWN:
            if event.key == pygame.K_z:
                mods = pygame.key.get_mods()
                if mods & pygame.KMOD_CTRL:
                    undo_move(board, last_move_row, last_move_col)
                    turn += 1
                    turn = turn % 2
        # tie
        if tie_move():
            pygame.mixer.music.load("event.ogg")
            pygame.mixer.music.play(0)
            game_over = True

        if game_over:
            # print(os.getpid())
            pygame.time.wait(3000)
            os.system("kill " + str(os.getpid()))
            os.system("./restart.sh")
