import os
from typing import Tuple

import pygame
from pygame import mixer
from pygame.gfxdraw import aacircle, filled_circle

from assets import yellow_coin, red_coin, black_coin, event_sound
from config import blue, black, white, red, yellow
from game_data import GameData


class GameRenderer:
    """
    Draws the current game state to the screen.
    """
    def __init__(self, screen, game_data: GameData):
        self.myfont = pygame.font.SysFont("monospace", 75)
        self.label = self.myfont.render("CONNECT FOUR!!", 1, white)
        screen.blit(self.label, (40, 10))
        self.screen = screen
        self.game_data = game_data

        pygame.display.set_caption("Connect Four | Mayank Singh")
        pygame.display.update()

    def draw_red_coin(self, x, y):
        self.screen.blit(red_coin, (x, y))

    def draw_yellow_coin(self, x, y):
        self.screen.blit(yellow_coin, (x, y))

    def draw_black_coin(self, x, y):
        self.screen.blit(black_coin, (x, y))

    def draw_coin(self, game_data, x, y):
        if game_data.turn == 0:
            self.screen.blit(red_coin, (x, y))
        else:
            self.screen.blit(yellow_coin, (x, y))

    def draw(self, game_data: GameData):
        if game_data.action == "tie":
            mixer.music.load(os.path.join("sounds", "event.ogg"))
            mixer.music.play(0)
            self.myfont = pygame.font.SysFont("monospace", 75)
            self.label = self.myfont.render("GAME DRAW !!!!", 1, white)
            self.screen.blit(self.label, (40, 10))
            pygame.display.update()
            game_data.action = None
        elif game_data.action == "undo":
            filled_circle(
                self.screen,
                game_data.last_move_row,
                game_data.last_move_col,
                self.game_data.radius,
                black
            )

            aacircle(
                self.screen,
                game_data.last_move_row,
                game_data.last_move_col,
                self.game_data.radius,
                black
            )

            self.draw_black_coin(
                game_data.last_move_col * self.game_data.sq_size + 5,
                self.game_data.height - (game_data.last_move_row * self.game_data.sq_size + self.game_data.sq_size - 5)
            )

            game_data.game_board.print_board()
            game_data.action = None
        elif game_data.action == "player_1_wins":
            self.label = self.myfont.render("PLAYER 1 WINS!", 1, red)
            self.screen.blit(self.label, (40, 10))

            mixer.music.load(event_sound)
            mixer.music.play(0)
            game_data.action = None
        elif game_data.action == "player_2_wins":
            self.label = self.myfont.render("PLAYER 2 WINS!", 1, yellow)
            self.screen.blit(self.label, (40, 10))

            mixer.music.load(event_sound)
            mixer.music.play(0)
            game_data.action = None

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
                    # mixer.music.load(disc_drop_1)
                    # mixer.music.play(0)
                elif board.board[r][c] == 2:
                    self.draw_yellow_coin(
                        int(c * sq_size) + 5, height - int(r * sq_size + sq_size - 5)
                    )
                    # mixer.music.load(disc_drop_2)
                    # mixer.music.play(0)

        pygame.display.update()
