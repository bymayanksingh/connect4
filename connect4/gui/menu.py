from __future__ import annotations

import random
from typing import Callable, Optional, Tuple

import pygame
from pygame.gfxdraw import aacircle, filled_circle

from connect4.config import (
    AMBER,
    CRIMSON,
    CYAN,
    EMERALD,
    PURPLE,
    SLATE_600,
    SLATE_700,
    SLATE_800,
    SLATE_850,
    WHITE,
)
from connect4.gui.assets import assets


class FloatingDisc:
    """Ambient floating disc drifting across menu background."""

    def __init__(self, bounds_w: int, bounds_h: int):
        self.bounds_w = bounds_w
        self.bounds_h = bounds_h
        self.x = random.uniform(20, bounds_w - 20)
        self.y = random.uniform(20, bounds_h - 20)
        self.radius = random.uniform(25, 60)
        self.vx = random.uniform(-25, 25)
        self.vy = random.uniform(-20, 20)
        self.color = random.choice([CRIMSON, AMBER, CYAN, EMERALD, PURPLE])
        self.alpha = random.randint(18, 42)

    def update(self, dt: float) -> None:
        self.x += self.vx * dt
        self.y += self.vy * dt
        if self.x - self.radius < -20 or self.x + self.radius > self.bounds_w + 20:
            self.vx *= -1
        if self.y - self.radius < -20 or self.y + self.radius > self.bounds_h + 20:
            self.vy *= -1

    def draw(self, screen: pygame.Surface) -> None:
        rad = int(self.radius)
        if rad < 2:
            return
        size = rad * 2
        surf = pygame.Surface((size, size), pygame.SRCALPHA)
        color_rgba = (self.color[0], self.color[1], self.color[2], self.alpha)
        filled_circle(surf, rad, rad, rad - 1, color_rgba)
        aacircle(surf, rad, rad, rad - 1, color_rgba)
        screen.blit(surf, (int(self.x - rad), int(self.y - rad)))


class Button:
    """Modern capsule UI button with smooth hover glow and sound feedback."""

    def __init__(
        self,
        text: str,
        x: int,
        y: int,
        width: int,
        height: int,
        action: Optional[Callable[[], None]] = None,
        color: Tuple[int, int, int] = SLATE_700,
        hover_color: Tuple[int, int, int] = CYAN,
        selected: bool = False,
        border_radius: int = 12,
    ):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.action = action
        self.color = color
        self.hover_color = hover_color
        self.selected = selected
        self.border_radius = border_radius
        self._hover_progress: float = 0.0

    def draw(self, screen: pygame.Surface, font: pygame.font.Font) -> None:
        mouse_pos = pygame.mouse.get_pos()
        is_hover = self.rect.collidepoint(mouse_pos)

        # Smooth hover interpolation
        target = 1.0 if is_hover else 0.0
        self._hover_progress += (target - self._hover_progress) * 0.35

        # Base card background
        bg_color = (
            int(SLATE_850[0] + (SLATE_800[0] - SLATE_850[0]) * self._hover_progress),
            int(SLATE_850[1] + (SLATE_800[1] - SLATE_850[1]) * self._hover_progress),
            int(SLATE_850[2] + (SLATE_800[2] - SLATE_850[2]) * self._hover_progress),
        )
        pygame.draw.rect(screen, bg_color, self.rect, border_radius=self.border_radius)

        # Border outline (Glows on hover or when selected)
        if self.selected:
            pygame.draw.rect(screen, EMERALD, self.rect, width=2, border_radius=self.border_radius)
            # Small green active indicator dot (Anti-aliased)
            filled_circle(screen, self.rect.left + 16, self.rect.centery, 4, EMERALD)
            aacircle(screen, self.rect.left + 16, self.rect.centery, 4, EMERALD)
        elif self._hover_progress > 0.05:
            # Subtle hover glow
            border_c = (
                int(SLATE_600[0] + (self.hover_color[0] - SLATE_600[0]) * self._hover_progress),
                int(SLATE_600[1] + (self.hover_color[1] - SLATE_600[1]) * self._hover_progress),
                int(SLATE_600[2] + (self.hover_color[2] - SLATE_600[2]) * self._hover_progress),
            )
            pygame.draw.rect(screen, border_c, self.rect, width=2, border_radius=self.border_radius)
        else:
            pygame.draw.rect(
                screen, self.color, self.rect, width=1, border_radius=self.border_radius
            )

        # Text label
        txt_color = WHITE if (is_hover or self.selected) else (210, 220, 235)
        text_surf = font.render(self.text, True, txt_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def handle_event(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                assets.play_sound("drop")
                if self.action:
                    self.action()
                return True
        return False
