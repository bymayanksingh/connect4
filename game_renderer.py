import os
from typing import Any, Optional, Union

import pygame
from pygame import mixer
from pygame.font import FontType
from pygame.ftfont import Font
from pygame.gfxdraw import aacircle, filled_circle

from assets import (black_coin, blue_coin, disc_drop_1, disc_drop_2,
                    event_sound, gray_coin, green_coin, red_coin, violet_coin,
                    yellow_coin)
from config import black, blue, gray, green, red, violet, white, yellow
from events import GameOver, MouseHoverEvent, PieceDropEvent, bus
from game_data import GameData


@bus.on("piece:drop")
def on_piece_drop(event: PieceDropEvent):
    """
    Plays a sound when a piece is dropped over an empty slot.
    :param event: Information about the drop, namely the slot where the piece was dropped.
    """
    if event.side == 1:
        mixer.music.load(disc_drop_1)
        mixer.music.play(0)

    if event.side == 2:
        mixer.music.load(disc_drop_2)
        mixer.music.play(0)


def coin_color(color):
    k = red_coin
    if color == green:
        k = green_coin
    elif color == blue:
        k = blue_coin
    elif color == violet:
        k = violet_coin
    elif color == yellow:
        k = yellow_coin
    elif color == gray:
        k = gray_coin

    return k
    

class GameRenderer:
    """
    Renders the current game state to the screen and the speakers.
    """

    game_data: GameData
    label: Optional[Any]
    myfont: Union[None, Font, FontType]

    def __init__(self, screen, game_data: GameData):
        """
        Initializes the game renderer.
        :param screen: The screen.
        :param game_data: All of the data for the game.
        """
        self.myfont = pygame.font.SysFont("monospace", 75)
        self.label = self.myfont.render("CONNECT FOUR!!", 1, white)
        screen.blit(self.label, (40, 10))
        self.screen = screen
        self.game_data = game_data

        pygame.display.set_caption("Connect Four | Mayank Singh")
        pygame.display.update()

    @bus.on("mouse:hover")
    def on_mouse_move(self, event: MouseHoverEvent):
        """
        Draws a coin over the slot that the mouse is positioned.
        :param event: Information about the hover, namely the x position
        """
        posx = event.posx

        pygame.draw.rect(
            self.screen, black, (0, 0, self.game_data.width, self.game_data.sq_size)
        )
        self.draw_coin(
            self.game_data,
            posx - (self.game_data.sq_size / 2),
            int(self.game_data.sq_size) - self.game_data.sq_size + 5,
        )

    def draw_coin_p1(self, x, y):
        """
        Draws the coin of player 1.
        :param x: The x position to draw the coin.
        :param y: The y position to draw the coin.
        """
        self.screen.blit(coin_color(self.game_data.c1), (x, y))

    def draw_coin_p2(self, x, y):
        """
        Draws the coin of player 2.
        :param x: The x position to draw the coin.
        :param y: The y position to draw the coin.
        """
        self.screen.blit(coin_color(self.game_data.c2), (x, y))

    def draw_black_coin(self, x, y):
        """
        Draws a black coin.
        :param x: The x position to draw the coin.
        :param y: The y position to draw the coin.
        """
        self.screen.blit(black_coin, (x, y))

    def draw_coin(self, game_data, x, y):
        """
        Draws a coin to the specified position
        using the color of the current player.

        :param game_data: All of the data for the game.
        :param x: The x position for the coin to be drawn.
        :param y: The y position for the coin to be drawn.
        """
        if game_data.turn == 0:
            self.screen.blit(coin_color(game_data.c1), (x, y))
        else:
            self.screen.blit(coin_color(game_data.c2), (x, y))

    def draw(self, game_data: GameData):
        """
        Draws the game state, including the board and the pieces.
        :param game_data: All of the data associated with the game.
        """
        if game_data.action == "undo":
            filled_circle(
                self.screen,
                game_data.last_move_row,
                game_data.last_move_col,
                self.game_data.radius,
                black,
            )

            aacircle(
                self.screen,
                game_data.last_move_row,
                game_data.last_move_col,
                self.game_data.radius,
                black,
            )

            self.draw_black_coin(
                game_data.last_move_col * self.game_data.sq_size + 5,
                self.game_data.height
                - (
                    game_data.last_move_row * self.game_data.sq_size
                    + self.game_data.sq_size
                    - 5
                ),
            )

            game_data.game_board.print_board()
            game_data.action = None

        self.draw_board(game_data.game_board)

    @bus.on("game:over")
    def on_game_over(self, event: GameOver):
        """
        Handles a game over event.
        :param event: Data about how the game ended.
        """
        color = None

        if event.winner == 1:
            color = self.game_data.c1
        if event.winner == 2:
            color = self.game_data.c2

        if not event.was_tie:
            self.label = self.myfont.render(f"PLAYER {event.winner} WINS!", 1, color)
            self.screen.blit(self.label, (40, 10))

            mixer.music.load(event_sound)
            mixer.music.play(0)
        else:
            mixer.music.load(os.path.join("sounds", "event.ogg"))
            mixer.music.play(0)
            self.myfont = pygame.font.SysFont("monospace", 75)
            self.label = self.myfont.render("GAME DRAW !!!!", 1, white)
            self.screen.blit(self.label, (40, 10))

    def draw_board(self, board):
        """
        Draws the game board to the screen.
        :param board: The game board.
        """
        sq_size = 100
        height = 700
        radius = int(sq_size / 2 - 5)

        for c in range(board.cols):
            for r in range(board.rows):
                pygame.draw.rect(
                    self.screen,
                    (self.game_data.bg),
                    (c * sq_size, (r + 1) * sq_size, sq_size, sq_size),
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

        for c in range(board.cols):
            for r in range(board.rows):
                if board.board[r][c] == 1:
                    self.draw_coin_p1(
                        int(c * sq_size) + 5, height - int(r * sq_size + sq_size - 5)
                    )

                elif board.board[r][c] == 2:
                    self.draw_coin_p2(
                        int(c * sq_size) + 5, height - int(r * sq_size + sq_size - 5)
                    )

        pygame.display.update()
