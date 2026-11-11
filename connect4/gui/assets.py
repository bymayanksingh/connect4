from __future__ import annotations

import random
from typing import Dict, Optional, Tuple

import pygame
from pygame.gfxdraw import aacircle, filled_circle

from connect4.config import (
    SOUNDS_DIR,
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
        self._muted = False
        self._init_mixer()

    def _init_mixer(self) -> None:
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            self._sound_enabled = True
        except Exception:
            self._sound_enabled = False

    def toggle_mute(self) -> bool:
        """Toggles sound mute state and returns current muted status."""
        self._muted = not self._muted
        return self._muted

    @property
    def is_muted(self) -> bool:
        return self._muted

    def get_coin_surface(
        self,
        color_rgb: Tuple[int, int, int],
        radius: int = 45,
        theme_name: Optional[str] = None,
    ) -> pygame.Surface:
        """
        Generates or retrieves a high-definition, photorealistic 3D acrylic chip
        with tactile concentric grooves, subtle bevels, and specular studio gloss,
        rendered using 2x supersampling (SSAA) for silky smooth anti-aliased curves.
        """
        cache_key = f"{color_rgb}_{radius}_{theme_name}"
        if cache_key in self._images:
            return self._images[cache_key]

        # 2x supersampling canvas for pristine anti-aliased geometry
        scale = 2
        hi_radius = radius * scale
        hi_size = hi_radius * 2
        hi_surf = pygame.Surface((hi_size, hi_size), pygame.SRCALPHA)
        hi_cx, hi_cy = hi_radius, hi_radius

        r, g, b = color_rgb
        # Outer rim / edge bevel
        dark_rim = (max(0, r - 75), max(0, g - 75), max(0, b - 75))
        filled_circle(hi_surf, hi_cx, hi_cy, hi_radius - 2, dark_rim)
        aacircle(hi_surf, hi_cx, hi_cy, hi_radius - 2, dark_rim)

        # Main disc base
        body_color = (min(255, r + 10), min(255, g + 10), min(255, b + 10))
        filled_circle(hi_surf, hi_cx, hi_cy, hi_radius - 6, body_color)
        aacircle(hi_surf, hi_cx, hi_cy, hi_radius - 6, body_color)

        # Concentric tactile groove 1 (Classic Connect 4 outer checker ring)
        groove1_r = max(8, int(hi_radius * 0.72))
        groove_dark = (max(0, r - 55), max(0, g - 55), max(0, b - 55))
        groove_light = (min(255, r + 55), min(255, g + 55), min(255, b + 55))
        pygame.draw.circle(hi_surf, groove_dark, (hi_cx, hi_cy), groove1_r, 4)
        pygame.draw.circle(hi_surf, groove_light, (hi_cx, hi_cy + 2), groove1_r - 2, 2)

        # Concentric tactile groove 2 (Inner ring)
        groove2_r = max(6, int(hi_radius * 0.44))
        pygame.draw.circle(hi_surf, groove_dark, (hi_cx, hi_cy), groove2_r, 4)
        pygame.draw.circle(hi_surf, groove_light, (hi_cx, hi_cy + 2), groove2_r - 2, 2)

        # Center subtle indented pip
        center_pip_r = max(4, int(hi_radius * 0.18))
        filled_circle(hi_surf, hi_cx, hi_cy, center_pip_r, groove_dark)
        aacircle(hi_surf, hi_cx, hi_cy, center_pip_r, groove_dark)

        # Specular studio gloss highlight arc across top-left
        gloss = pygame.Surface((hi_size, hi_size), pygame.SRCALPHA)
        highlight_rect = pygame.Rect(
            int(hi_radius * 0.28),
            int(hi_radius * 0.16),
            int(hi_radius * 0.95),
            int(hi_radius * 0.48),
        )
        pygame.draw.ellipse(gloss, (255, 255, 255, 80), highlight_rect)
        hi_surf.blit(gloss, (0, 0))

        # Downsample with bilinear smoothscale for flawless edge filtering
        surf = pygame.transform.smoothscale(hi_surf, (radius * 2, radius * 2))
        self._images[cache_key] = surf
        return surf

    def play_sound(self, sound_name: str) -> None:
        """Plays sound effect safely with exception swallowing and alias routing."""
        if not self._sound_enabled or self._muted:
            return

        # Route aliases
        target_name = sound_name
        if sound_name == "drop":
            target_name = random.choice(["disc_drop_1", "disc_drop_2"])
        elif sound_name in ("win", "victory"):
            target_name = "event"

        if target_name not in self._sounds:
            # Check sound file extensions
            for ext in (".wav", ".ogg", ".mp3"):
                sound_file = SOUNDS_DIR / f"{target_name}{ext}"
                if sound_file.exists():
                    try:
                        snd = pygame.mixer.Sound(str(sound_file))
                        # Adjust default volume levels
                        if "drop" in target_name:
                            snd.set_volume(0.65)
                        elif target_name == "event":
                            snd.set_volume(0.85)
                        self._sounds[target_name] = snd
                        break
                    except Exception:
                        pass
            else:
                self._sounds[target_name] = None

        snd = self._sounds.get(target_name)
        if snd:
            try:
                snd.play()
            except Exception:
                pass


# Global singleton asset manager
assets = AssetManager()
