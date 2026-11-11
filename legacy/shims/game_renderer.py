"""
Backward compatibility layer for legacy game_renderer.py.
For modern development, import directly from connect4.gui.renderer.
"""
from connect4.gui.renderer import GameRenderer, ConsoleBuffer

console = ConsoleBuffer()

__all__ = ["GameRenderer", "ConsoleBuffer", "console"]
