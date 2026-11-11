from __future__ import annotations

from typing import Callable, List, Optional, Tuple
import pygame

from connect4.config import (
    BLACK,
    BLUE,
    BOARD_PRESETS,
    COLOR_THEMES,
    GREEN,
    LIGHT_BLUE,
    RED,
    WHITE,
    YELLOW,
)
from connect4.gui.assets import assets
from connect4.types import AIDifficulty, BoardDimensions, GameMode


class Button:
    """Clickable UI button with hover states, sound feedback, and active highlights."""

    def __init__(
        self,
        text: str,
        x: int,
        y: int,
        width: int,
        height: int,
        action: Optional[Callable[[], None]] = None,
        color: Tuple[int, int, int] = WHITE,
        hover_color: Tuple[int, int, int] = LIGHT_BLUE,
        selected: bool = False,
    ):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.action = action
        self.color = color
        self.hover_color = hover_color
        self.selected = selected

    def draw(self, screen: pygame.Surface, font: pygame.font.Font) -> None:
        mouse_pos = pygame.mouse.get_pos()
        is_hover = self.rect.collidepoint(mouse_pos)
        draw_color = self.hover_color if is_hover else self.color

        if self.selected:
            pygame.draw.rect(screen, GREEN, (self.rect.x - 4, self.rect.y - 4, self.rect.width + 8, self.rect.height + 8), border_radius=6)

        pygame.draw.rect(screen, draw_color, self.rect, border_radius=6)
        # Inner dark fill
        inner_rect = pygame.Rect(self.rect.x + 2, self.rect.y + 2, self.rect.width - 4, self.rect.height - 4)
        pygame.draw.rect(screen, BLACK, inner_rect, border_radius=5)

        text_surf = font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def handle_event(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                assets.play_sound("select")
                if self.action:
                    self.action()
                return True
        return False
