"""
Backward compatibility layer for legacy assets.py.
For modern development, import directly from connect4.gui.assets.
"""
from pathlib import Path
from connect4.config import IMAGES_DIR, SOUNDS_DIR
from connect4.gui.assets import assets, AssetManager

red_coin = str(IMAGES_DIR / "redball90px.png")
yellow_coin = str(IMAGES_DIR / "yellowball90px.png")
black_coin = str(IMAGES_DIR / "blackball91px.png")
disc_drop_1 = str(SOUNDS_DIR / "drop.wav")
disc_drop_2 = str(SOUNDS_DIR / "drop.wav")
event_sound = str(SOUNDS_DIR / "win.wav")

__all__ = [
    "assets",
    "AssetManager",
    "red_coin",
    "yellow_coin",
    "black_coin",
    "disc_drop_1",
    "disc_drop_2",
    "event_sound",
]
