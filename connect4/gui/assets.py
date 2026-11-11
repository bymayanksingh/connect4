from __future__ import annotations

import os
from pathlib import Path
from typing import Dict, Optional, Tuple
import pygame

from connect4.config import (
    ASSETS_DIR,
    COLOR_THEMES,
    IMAGES_DIR,
    SOUNDS_DIR,
    BLACK,
    WHITE,
    BLUE,
    RED,
    YELLOW,
)


class AssetManager:
    """
    Robust asset loader for sprites, themes, and sound effects.
    Features procedural surface generation fallbacks so the UI never crashes
    if external media assets are missing.
    """

    def __init__(self):
        self._images: Dict[str, pygame.Surface] = {}
        self._sounds: Dict[str, Optional[pygame.mixer.Sound]] = {}
        self._sound_enabled = False
        self._init_mixer()

    def _init_mixer(self) -> None:
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            self._sound_enabled = True
        except Exception:
            self._sound_enabled = False

    def get_coin_surface(
        self,
        color_rgb: Tuple[int, int, int],
        radius: int = 45,
        theme_name: Optional[str] = None,
    ) -> pygame.Surface:
        """
        Loads coin sprite or draws an anti-aliased procedural chip surface.
        """
        cache_key = f"{color_rgb}_{radius}_{theme_name}"
        if cache_key in self._images:
            return self._images[cache_key]

        # Check if theme file exists
        if theme_name and theme_name in COLOR_THEMES:
            filename = COLOR_THEMES[theme_name][1]
            img_path = IMAGES_DIR / filename
            if img_path.exists():
                try:
                    loaded = pygame.image.load(str(img_path)).convert_alpha()
                    scaled = pygame.transform.smoothscale(loaded, (radius * 2, radius * 2))
                    self._images[cache_key] = scaled
                    return scaled
                except Exception:
                    pass

        # Procedural fallback
        surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        # Outer border
        pygame.draw.circle(surf, (30, 30, 30), (radius, radius), radius)
        # Inner colored coin
        pygame.draw.circle(surf, color_rgb, (radius, radius), radius - 3)
        # Subtle highlight reflection
        highlight_color = (
            min(255, color_rgb[0] + 50),
            min(255, color_rgb[1] + 50),
            min(255, color_rgb[2] + 50),
        )
        pygame.draw.circle(surf, highlight_color, (radius - radius // 4, radius - radius // 4), radius // 3)

        self._images[cache_key] = surf
        return surf

    def play_sound(self, sound_name: str) -> None:
        """Plays sound effect safely with exception swallowing."""
        if not self._sound_enabled:
            return

        if sound_name not in self._sounds:
            sound_file = SOUNDS_DIR / f"{sound_name}.wav"
            if not sound_file.exists():
                sound_file = SOUNDS_DIR / f"{sound_name}.mp3"

            if sound_file.exists():
                try:
                    self._sounds[sound_name] = pygame.mixer.Sound(str(sound_file))
                except Exception:
                    self._sounds[sound_name] = None
            else:
                self._sounds[sound_name] = None

        snd = self._sounds.get(sound_name)
        if snd:
            try:
                snd.play()
            except Exception:
                pass


# Global singleton asset manager
assets = AssetManager()
