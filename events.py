"""
Backward compatibility layer for legacy events.py.
For modern development, import directly from connect4.events.
"""
from connect4.events import (
    bus,
    MouseHoverEvent,
    MouseClickEvent,
    GameOver,
    PieceDropEvent,
    UndoEvent,
)

__all__ = [
    "bus",
    "MouseHoverEvent",
    "MouseClickEvent",
    "GameOver",
    "PieceDropEvent",
    "UndoEvent",
]
