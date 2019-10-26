
"""
Holds the global event bus and the classes holding data for the event messages.
"""

from event_bus import EventBus
bus = EventBus()

class MouseHoverEvent:
    """
    Fired when a user has moved their mouse to place a piece.
    """
    def __init__(self, posx):
        self.posx = posx


class MouseClickEvent:
    """
    Fired when the user has clicked the mouse.
    """
    def __init__(self, posx):
        self.posx = posx


class GameOver:
    """
    Fired when the game is over, including tie games.
    """
    def __init__(self, was_tie=True, winner=None):
        self.was_tie = was_tie
        self.winner = winner


class PieceDropEvent:
    """
    Fired when a game piece is dropped into an open slot.
    """
    def __init__(self, side):
        self.side = side
