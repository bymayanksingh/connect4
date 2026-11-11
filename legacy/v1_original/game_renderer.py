import os
from typing import Any, Optional, Union

import pygame
from pygame import mixer
from pygame.font import FontType
from pygame.ftfont import Font
from pygame.gfxdraw import aacircle, filled_circle

from assets import (black_coin, disc_drop_1, disc_drop_2, event_sound,
                    red_coin, yellow_coin)
from config import BLACK, BLUE, RED, WHITE, YELLOW
from events import GameOver, MouseHoverEvent, PieceDropEvent, bus
from game_data import GameData

# at the very top of game_renderer.py
import sys

class ConsoleBuffer:
    def __init__(self):
        self.lines: list[str] = []

    def write(self, txt: str):
        for line in txt.splitlines():
            self.lines.append(line)

    def flush(self):
        pass

# instantiate and redirect stdout
console = ConsoleBuffer()
sys.stdout = console


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
        self.myfont = pygame.font.SysFont("monospace", 75)
        self.label = self.myfont.render("CONNECT FOUR!!", 1, WHITE)
        screen.blit(self.label, (40, 10))
        self.screen = screen
        self.game_data = game_data

        self.console = console

        self.font = pygame.font.Font(None, 20)
        line_h = self.font.get_linesize()
        self.line_height = line_h
        self.scroll_index = max(0, len(console.lines) - self.line_height)

        pygame.display.set_caption("Connect Four | Mayank Singh")
        pygame.display.update()

    def draw_stats_panel(self):
        panel_x = self.game_data.width - self.game_data.panel_size
        panel_w = self.game_data.panel_size
        panel_h = self.game_data.height

        # 1) clear panel
        self.screen.fill(BLACK, (panel_x, 0, panel_w, panel_h))

        # 2) figure out how many lines fit
        visible_lines = panel_h // self.line_height
        total = len(console.lines)
        max_start = max(0, total - visible_lines)
        # clamp scroll
        self.scroll_index = min(self.scroll_index, max_start)

        # 3) draw the slice from top of panel
        for i, line in enumerate(console.lines[self.scroll_index:self.scroll_index + visible_lines]):
            txt = self.font.render(line, True, WHITE)
            y = 0 + i * self.line_height
            self.screen.blit(txt, (panel_x + 8, y))

        # 4) full‐height scrollbar
        track_w = 6
        track_x = panel_x + panel_w - track_w - 4
        pygame.draw.rect(self.screen, (40, 40, 40),
                         (track_x, 0, track_w, panel_h))
        if total > visible_lines:
            thumb_h = panel_h * (visible_lines / total)
            thumb_y = (panel_h - thumb_h) * (self.scroll_index / max_start)
            pygame.draw.rect(self.screen, (200, 200, 200),
                             (track_x, thumb_y, track_w, thumb_h))

    @bus.on("mouse:hover")
    def on_mouse_hover(self, event: MouseHoverEvent):
        """
        Draws a coin over the slot that the mouse is positioned.
        :param event: Information about the hover, namely the x position
        """
        posx = event.posx
        
        # Make sure we're within the valid column range
        if posx >= self.game_data.cols * self.game_data.sq_size:
            # Mouse is outside the play area (in stats panel)
            return

        pygame.draw.rect(
            self.screen, BLACK, (0, 0, self.game_data.width, self.game_data.sq_size)
        )
        self.draw_coin(
            self.game_data,
            posx - (self.game_data.sq_size / 2),
            int(self.game_data.sq_size) - self.game_data.sq_size + 5,
        )

    def draw_red_coin(self, x, y):
        """
        Draws a red coin.
        :param x: The x position to draw the coin.
        :param y: The y position to draw the coin.
        """
        self.screen.blit(red_coin, (x, y))

    def draw_yellow_coin(self, x, y):
        """
        Draws a yellow coin.
        :param x: The x position to draw the coin.
        :param y: The y position to draw the coin.
        """
        self.screen.blit(yellow_coin, (x, y))

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
            self.screen.blit(red_coin, (x, y))
        else:
            self.screen.blit(yellow_coin, (x, y))

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
                BLACK,
            )

            aacircle(
                self.screen,
                game_data.last_move_row,
                game_data.last_move_col,
                self.game_data.radius,
                BLACK,
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
            color = RED
        if event.winner == 2:
            color = YELLOW

        if not event.was_tie:
            self.label = self.myfont.render(f"PLAYER {event.winner} WINS!", 1, color)
            self.screen.blit(self.label, (40, 10))

            mixer.music.load(event_sound)
            mixer.music.play(0)
        else:
            mixer.music.load(os.path.join("sounds", "event.ogg"))
            mixer.music.play(0)
            self.myfont = pygame.font.SysFont("monospace", 75)
            self.label = self.myfont.render("GAME DRAW !!!!", 1, WHITE)
            self.screen.blit(self.label, (40, 10))

    def draw_board(self, board):
        """
        Draws the game board to the screen.
        :param board: The game board.
        """
        sq_size = self.game_data.sq_size
        height = self.game_data.height
        radius = self.game_data.radius

        for c in range(board.cols):
            for r in range(board.rows):
                pygame.draw.rect(
                    self.screen,
                    BLUE,
                    (c * sq_size, (r + 1) * sq_size, sq_size, sq_size),
                )
                aacircle(
                    self.screen,
                    int(c * sq_size + sq_size / 2),
                    int((r + 1) * sq_size + sq_size / 2),
                    radius,
                    BLACK,
                )
                filled_circle(
                    self.screen,
                    int(c * sq_size + sq_size / 2),
                    int((r + 1) * sq_size + sq_size / 2),
                    radius,
                    BLACK,
                )

        for c in range(board.cols):
            for r in range(board.rows):
                if board.board[r][c] == 1:
                    self.draw_red_coin(
                        int(c * sq_size) + 5, height - int(r * sq_size + sq_size - 5)
                    )

                elif board.board[r][c] == 2:
                    self.draw_yellow_coin(
                        int(c * sq_size) + 5, height - int(r * sq_size + sq_size - 5)
                    )
        
        # Display the game mode and board size info
        font = pygame.font.SysFont(None, 24)
        x_offset = self.game_data.width - self.game_data.panel_size + 20
        y = height - 140
        
        # Draw game information
        """game_mode_text = f"Game Mode: {self.game_data.game_mode.upper()}"
        board_size_text = f"Board Size: {self.game_data.cols}x{self.game_data.rows}"
        win_condition_text = f"Win Condition: {self.game_data.win_condition} in a row"
        
        self.screen.blit(font.render(game_mode_text, True, WHITE), (x_offset, y))
        self.screen.blit(font.render(board_size_text, True, WHITE), (x_offset, y + 30))
        self.screen.blit(font.render(win_condition_text, True, WHITE), (x_offset, y + 60))"""

        self.draw_stats_panel()
        pygame.display.update()
