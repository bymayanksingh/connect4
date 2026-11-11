from __future__ import annotations

from typing import Any

from event_bus import EventBus

# Global event bus instance for backward compatibility with existing code
bus = EventBus()


class MouseHoverEvent:
    """Event fired when a user moves the mouse over the game board."""

    def __init__(self, posx: int):
        self.posx = posx


class MouseClickEvent:
    """Event fired when the user clicks the mouse on the game board."""

    def __init__(self, posx: int):
        self.posx = posx


class GameOver:
    """Event fired when the game is over, including tie games."""

    def __init__(self, was_tie: bool = True, winner: Any = None):
        self.was_tie = was_tie
        self.winner = winner


class PieceDropEvent:
    """Event fired when a game piece is dropped into an open slot."""

    def __init__(self, side: Any):
        self.side = side


class UndoEvent:
    """Event fired when an undo action is requested."""

    def __init__(self):
        pass
