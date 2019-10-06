import pygame
from pygame.gfxdraw import aacircle, filled_circle

from assets import yellow_coin, red_coin, black_coin
from config import blue, black
from game_data import GameData


class GameRenderer:
    def __init__(self, screen):
        self.screen = screen

    def draw_black_coin(self, x, y):
        self.draw_coin(black_coin, x, y)

    def draw_red_coin(self, x, y):
        self.draw_coin(red_coin, x, y)

    def draw_yellow_coin(self, x, y):
        self.draw_coin(yellow_coin, x, y)

    def draw_coin(self, coin, x, y):
        self.screen.blit(coin, (x, y))

    def draw(self, game_data: GameData):
        self.draw_board(game_data.game_board)

    def draw_board(self, board):
        sq_size = 100
        height = 700
        radius = int(sq_size / 2 - 5)

        for c in range(board.cols):
            for r in range(board.rows):
                pygame.draw.rect(
                    self.screen, blue, (c * sq_size, (r + 1) * sq_size, sq_size, sq_size)
                )
                aacircle(
                    self.screen,
                    int(c * sq_size + sq_size / 2),
                    int((r + 1) * sq_size + sq_size / 2),
                    radius,
                    black,
                )
                filled_circle(
                    self.screen,
                    int(c * sq_size + sq_size / 2),
                    int((r + 1) * sq_size + sq_size / 2),
                    radius,
                    black,
                )
                # pygame.draw.circle(screen, black, (int(c*sq_size + sq_size/2), int((r+1) * sq_size + sq_size/2)), radius)

        for c in range(board.cols):
            for r in range(board.rows):
                if board.board[r][c] == 1:
                    self.draw_red_coin(
                        int(c * sq_size) + 5, height - int(r * sq_size + sq_size - 5)
                    )
                    #mixer.music.load(disc_drop_1)
                    #mixer.music.play(0)
                elif board.board[r][c] == 2:
                    self.draw_yellow_coin(
                        int(c * sq_size) + 5, height - int(r * sq_size + sq_size - 5)
                    )
                    #mixer.music.load(disc_drop_2)
                    #mixer.music.play(0)

        pygame.display.update()
