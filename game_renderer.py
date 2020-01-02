import os
from typing import Any, Optional, Union

import pygame
import time
from pygame import mixer
from pygame.font import FontType
from pygame.ftfont import Font
from pygame.gfxdraw import aacircle, filled_circle

from assets import (
    black_coin,
    board_pattern,
    disc_drop_1,
    disc_drop_2,
    event_sound,
    red_coin,
    yellow_coin,
)
from config import black, blue, red, white, yellow
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
        self.game_data = game_data
        self.screen = screen

        self.myfont = pygame.font.SysFont("monospace", self.game_data.font_size)
        message = "CONNECT FOUR!"
        self.label = self.myfont.render(message, 1, white)
        self.screen.blit(self.label, ((self.game_data.width - len(message)*self.game_data.character_width)//2, 
        self.game_data.margin))

        pygame.display.set_caption("Connect Four | Mayank Singh")
        pygame.display.update()

    @bus.on("mouse:hover")
    def on_mouse_move(self, event: MouseHoverEvent):
        """
        Draws a coin over the slot that the mouse is positioned.
        :param event: Information about the hover, namely the x position
        """
        posx = event.posx
        self.game_data.posx = event.posx

        pygame.draw.rect(
            self.screen, black, (0, 0, self.game_data.width, self.game_data.sq_size)
        )
        self.draw_coin(
            self.game_data,
            posx - self.game_data.radius, self.game_data.margin,
        )

    def draw_red_coin(self, x, y):
        """
        Draws a red coin.
        :param x: The x position to draw the coin.
        :param y: The y position to draw the coin.
        """
        radius = self.game_data.radius
        sq_size = self.game_data.sq_size
        self.screen.blit(pygame.transform.scale(red_coin, (2*radius, 2*radius)), (x, y))

    def draw_yellow_coin(self, x, y):
        """
        Draws a yellow coin.
        :param x: The x position to draw the coin.
        :param y: The y position to draw the coin.
        """
        radius = self.game_data.radius
        sq_size = self.game_data.sq_size
        self.screen.blit(pygame.transform.scale(yellow_coin, (2*radius, 2*radius)), (x, y))

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
            radius = game_data.radius
            sq_size = game_data.sq_size
            self.screen.blit(pygame.transform.scale(red_coin, (2*radius, 2*radius)), (x, y))
        else:
            radius = game_data.radius
            sq_size = game_data.sq_size
            self.screen.blit(pygame.transform.scale(yellow_coin, (2*radius, 2*radius)), (x, y))

    def draw(self, game_data: GameData):
        """
        Draws the game state, including the board and the pieces.
        :param game_data: All of the data associated with the game.
        """
        self.draw_board(game_data)

    @bus.on("game:over")
    def on_game_over(self, event: GameOver):
        """
        Handles a game over event.
        :param event: Data about how the game ended.
        """
        color = None

        if event.winner == 1:
            color = red
        if event.winner == 2:
            color = yellow

        if not event.was_tie:
            message = f"PLAYER {event.winner} WINS!"
            self.label = self.myfont.render(message, 1, color)
            self.screen.blit(self.label, ((self.game_data.width - len(message)*self.game_data.character_width)//2, 
        self.game_data.margin))

            mixer.music.load(event_sound)
            mixer.music.play(0)
        else:
            message = "GAME DRAW!"
            self.label = self.myfont.render(message, 1, white)
            self.screen.blit(self.label, ((self.game_data.width - len(message)*self.game_data.character_width)//2, 
        self.game_data.margin))

            mixer.music.load(os.path.join("sounds", "event.ogg"))
            mixer.music.play(0)

    def drop_piece(self, row, col, turn):
        """
        Animates the falling piece
        :param row: The row in which the piece will land
        :param col: The column in which the piece will fall
        :param turn: Which player's coin fell
        """
        sq_size = self.game_data.sq_size
        radius = self.game_data.radius

        y = 0
        acc = self.game_data.height*8
        y_max = 0 + self.game_data.game_board.rows*sq_size - (row)*sq_size
        delta_t = 0.005

        t = 0
        while(t<10):
            t += delta_t
            y = 0.5*acc*(t**2)
            if(y>=y_max):
                pygame.draw.rect(
                    self.screen,
                    black,
                    (0,0, self.game_data.width, sq_size)
                )
                break
            time.sleep(delta_t)
            pygame.draw.rect(
                self.screen,
                black,
                (col*sq_size, 0, sq_size, self.game_data.game_board.rows*sq_size - (row)*sq_size)
            )
            if turn==1:
                self.draw_red_coin(
                    int(col * sq_size) + self.game_data.margin, int(y)
                )

            elif turn==2:
                self.draw_yellow_coin(
                    int(col * sq_size) + self.game_data.margin, int(y)
                )
                
            for r in range(self.game_data.game_board.rows - row):
                self.screen.blit(pygame.transform.scale(board_pattern, (sq_size, sq_size)), (col*sq_size, (r+1)*sq_size))
            pygame.display.update()

    def draw_board(self, data):
        """
        Draws the game board to the screen.
        :param data: All data associated with the game.
        """

        board = data.game_board

        sq_size = data.sq_size
        height = data.height
        radius = data.radius
        
        pygame.draw.rect(
                            self.screen,
                            black,
                            (0, sq_size, self.game_data.width, self.game_data.height)
                        )
        for c in range(board.cols):
            for r in range(board.rows):
                self.screen.blit(pygame.transform.scale(board_pattern, (sq_size, sq_size)), (c*sq_size, (r+1)*sq_size))

        for c in range(board.cols):
            for r in range(board.rows):
                if board.board[r][c] == 1:
                    self.draw_red_coin(
                        int(c * sq_size) + self.game_data.margin, height - int(r * sq_size + sq_size - self.game_data.margin)
                    )

                elif board.board[r][c] == 2:
                    self.draw_yellow_coin(
                        int(c * sq_size) + self.game_data.margin, height - int(r * sq_size + sq_size - self.game_data.margin)
                    )

        pygame.display.update()
