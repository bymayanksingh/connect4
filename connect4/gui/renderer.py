from __future__ import annotations

import math
from typing import Any, List, Optional, Tuple
import pygame
from pygame.gfxdraw import aacircle, filled_circle

from connect4.board import GameBoard
from connect4.config import (
    ANIMATION_SPEED,
    BLACK,
    BLUE,
    COLOR_THEMES,
    DARK_BLUE,
    DARK_GRAY,
    DEFAULT_DISC_RADIUS,
    DEFAULT_SQ_SIZE,
    GRAY,
    GREEN,
    LIGHT_BLUE,
    RED,
    WHITE,
    YELLOW,
)
from connect4.game import Connect4Game
from connect4.gui.assets import assets
from connect4.types import GameStatus, Player


class ConsoleBuffer:
    """In-game terminal logs buffer for the GUI stats panel."""

    def __init__(self, max_lines: int = 500):
        self.lines: List[str] = []
        self.max_lines = max_lines

    def log(self, text: str) -> None:
        for line in str(text).splitlines():
            self.lines.append(line)
        if len(self.lines) > self.max_lines:
            self.lines = self.lines[-self.max_lines:]

    def clear(self) -> None:
        self.lines.clear()


class GameRenderer:
    """
    Renders Connect 4 boards, pieces, hover cursors, drop animations,
    winning line highlights, and debug console panels.
    """

    def __init__(
        self,
        screen: pygame.Surface,
        sq_size: int = DEFAULT_SQ_SIZE,
        p1_theme: str = "red",
        p2_theme: str = "yellow",
        board_color: Tuple[int, int, int] = BLUE,
        show_console: bool = False,
    ):
        self.screen = screen
        self.sq_size = sq_size
        self.radius = int(sq_size / 2 - 5)
        self.p1_theme = p1_theme
        self.p2_theme = p2_theme
        self.board_color = board_color
        self.show_console = show_console
        self.console = ConsoleBuffer()
        self.scroll_index = 0
        self.hover_x: Optional[int] = None
        self._init_fonts()

    def _init_fonts(self) -> None:
        if not pygame.font.get_init():
            pygame.font.init()
        self.title_font = pygame.font.SysFont("monospace", int(self.sq_size * 0.45), bold=True)
        self.msg_font = pygame.font.SysFont("monospace", int(self.sq_size * 0.35), bold=True)
        self.console_font = pygame.font.SysFont("monospace", 14)

    def get_p1_color(self) -> Tuple[int, int, int]:
        return COLOR_THEMES.get(self.p1_theme, (RED, ""))[0]

    def get_p2_color(self) -> Tuple[int, int, int]:
        return COLOR_THEMES.get(self.p2_theme, (YELLOW, ""))[0]

    def set_hover_pos(self, mouse_x: int) -> None:
        self.hover_x = mouse_x

    def draw_board(self, game: Connect4Game, winning_coords: Optional[List[Tuple[int, int]]] = None) -> None:
        board = game.board
        width = board.cols * self.sq_size
        height = (board.rows + 1) * self.sq_size

        # Top area (where piece hovers)
        pygame.draw.rect(self.screen, BLACK, (0, 0, width, self.sq_size))

        # Hover piece
        if not game.is_game_over and self.hover_x is not None:
            # Constrain hover_x within board boundaries
            clamped_x = max(self.sq_size // 2, min(self.hover_x, width - self.sq_size // 2))
            hover_color = self.get_p1_color() if game.current_player == Player.P1 else self.get_p2_color()
            hover_theme = self.p1_theme if game.current_player == Player.P1 else self.p2_theme
            coin_surf = assets.get_coin_surface(hover_color, self.radius, hover_theme)
            self.screen.blit(coin_surf, (clamped_x - self.radius, self.sq_size // 2 - self.radius))

        # Blue Board Grid Frame
        win_set = set(winning_coords or [])
        for c in range(board.cols):
            for r in range(board.rows):
                rect_x = c * self.sq_size
                rect_y = (r + 1) * self.sq_size

                # Draw blue cell square
                pygame.draw.rect(self.screen, self.board_color, (rect_x, rect_y, self.sq_size, self.sq_size))

                # Draw slot circle (In Pygame, r=0 is top visual row, whereas board row 0 is bottom)
                # Translate board coordinates: visual_r = board.rows - 1 - r
                board_r = board.rows - 1 - r
                cell_val = board.board[board_r][c]
                center_x = rect_x + self.sq_size // 2
                center_y = rect_y + self.sq_size // 2

                if cell_val == 1:
                    coin_surf = assets.get_coin_surface(self.get_p1_color(), self.radius, self.p1_theme)
                    self.screen.blit(coin_surf, (center_x - self.radius, center_y - self.radius))
                elif cell_val == 2:
                    coin_surf = assets.get_coin_surface(self.get_p2_color(), self.radius, self.p2_theme)
                    self.screen.blit(coin_surf, (center_x - self.radius, center_y - self.radius))
                else:
                    # Empty circle cutout
                    filled_circle(self.screen, center_x, center_y, self.radius, BLACK)
                    aacircle(self.screen, center_x, center_y, self.radius, BLACK)

                # Winning chip highlight
                if (board_r, c) in win_set:
                    pygame.draw.circle(self.screen, GREEN, (center_x, center_y), self.radius + 2, 4)

        # Draw Console panel if enabled
        if self.show_console:
            self._draw_console(width, height)

    def _draw_console(self, board_width: int, board_height: int) -> None:
        console_width = 300
        console_rect = pygame.Rect(board_width, 0, console_width, board_height)
        pygame.draw.rect(self.screen, DARK_GRAY, console_rect)
        pygame.draw.line(self.screen, WHITE, (board_width, 0), (board_width, board_height), 2)

        # Title
        hdr = self.console_font.render("AGENT DIAGNOSTICS", True, YELLOW)
        self.screen.blit(hdr, (board_width + 10, 10))

        y_offset = 35
        visible_lines = self.console.lines[-25:]
        for line in visible_lines:
            text_surf = self.console_font.render(line[:35], True, WHITE)
            self.screen.blit(text_surf, (board_width + 10, y_offset))
            y_offset += 18

    def draw_game_over(self, game: Connect4Game) -> None:
        board = game.board
        width = board.cols * self.sq_size

        if game.status == GameStatus.DRAW:
            msg = "IT'S A DRAW!"
            color = WHITE
        elif game.status == GameStatus.WIN_P1:
            msg = "PLAYER 1 WINS!"
            color = self.get_p1_color()
        else:
            msg = "PLAYER 2 WINS!"
            color = self.get_p2_color()

        text_surf = self.title_font.render(msg, True, color)
        text_rect = text_surf.get_rect(center=(width // 2, self.sq_size // 2))
        pygame.draw.rect(self.screen, BLACK, (0, 0, width, self.sq_size))
        self.screen.blit(text_surf, text_rect)
