from __future__ import annotations

from pathlib import Path
from typing import Dict, Tuple

# Base repository and asset paths
PACKAGE_ROOT = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_ROOT.parent
ASSETS_DIR = REPO_ROOT / "assets"
IMAGES_DIR = ASSETS_DIR / "images"
SOUNDS_DIR = ASSETS_DIR / "sounds"

# Standard & Modern Design System RGB Colors
BLACK: Tuple[int, int, int] = (0, 0, 0)
WHITE: Tuple[int, int, int] = (255, 255, 255)
BLUE: Tuple[int, int, int] = (0, 0, 255)
RED: Tuple[int, int, int] = (255, 0, 0)
GREEN: Tuple[int, int, int] = (0, 255, 0)
YELLOW: Tuple[int, int, int] = (255, 255, 0)
GRAY: Tuple[int, int, int] = (128, 128, 128)
DARK_GRAY: Tuple[int, int, int] = (50, 50, 50)
LIGHT_BLUE: Tuple[int, int, int] = (23, 196, 243)
VIOLET: Tuple[int, int, int] = (138, 43, 226)
NEON_BLUE: Tuple[int, int, int] = (0, 255, 255)
DARK_BLUE: Tuple[int, int, int] = (0, 0, 139)

# Modern UI / Dark Mode Palette
SLATE_950: Tuple[int, int, int] = (9, 13, 22)
SLATE_900: Tuple[int, int, int] = (15, 23, 42)
SLATE_850: Tuple[int, int, int] = (23, 32, 51)
SLATE_800: Tuple[int, int, int] = (30, 41, 59)
SLATE_700: Tuple[int, int, int] = (51, 65, 85)
SLATE_600: Tuple[int, int, int] = (71, 85, 105)
BOARD_BLUE_TOP: Tuple[int, int, int] = (37, 99, 235)
BOARD_BLUE_MID: Tuple[int, int, int] = (29, 78, 216)
BOARD_BLUE_DARK: Tuple[int, int, int] = (30, 58, 138)
BOARD_BLUE_RIM: Tuple[int, int, int] = (96, 165, 250)
GOLD: Tuple[int, int, int] = (245, 158, 11)
AMBER: Tuple[int, int, int] = (251, 191, 36)
CRIMSON: Tuple[int, int, int] = (239, 68, 68)
EMERALD: Tuple[int, int, int] = (16, 185, 129)
CYAN: Tuple[int, int, int] = (6, 182, 212)
PURPLE: Tuple[int, int, int] = (168, 85, 247)

# Backward-compatibility aliases
black = BLACK
white = WHITE
blue = BLUE
red = RED
green = GREEN
yellow = YELLOW
grey = GRAY

# Color Themes mapping to asset filenames
COLOR_THEMES: Dict[str, Tuple[Tuple[int, int, int], str]] = {
    "red": (RED, "red.png"),
    "yellow": (YELLOW, "Yellow.png"),
    "green": (GREEN, "green.png"),
    "violet": (VIOLET, "Violet.png"),
    "neonBlue": (NEON_BLUE, "neonBlue.png"),
    "darkBlue": (DARK_BLUE, "darkBlue.png"),
    "gray": (GRAY, "gray.png"),
}

# Display constants
DEFAULT_SQ_SIZE: int = 100
DEFAULT_DISC_RADIUS: int = int(DEFAULT_SQ_SIZE / 2 - 5)
DEFAULT_FPS: int = 60
ANIMATION_SPEED: int = 25  # Pixels per frame for coin drop animation

# Board Presets: (cols, rows, win_condition)
BOARD_PRESETS = {
    "standard": (7, 6, 4),
    "mini": (4, 3, 3),
    "large": (8, 7, 4),
    "challenge": (7, 6, 5),
}
