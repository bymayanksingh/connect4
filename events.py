"""
Holds the global event bus and the classes holding data for the event messages.
"""

from event_bus import EventBus

# Initialize the global event bus.
bus = EventBus()


class MouseHoverEvent:
    """Event fired when a user moves the mouse over the game board.

    Args:
        posx (int): The coordinate of the mouse pointer.
    """
    def __init__(self, posx: int):
        self.posx = posx


class MouseClickEvent:
    """Event fired when the user clicks the mouse on the game board.

    Args:
        posx (int): The coordinate of the mouse click.
    """
    def __init__(self, posx: int):
        self.posx = posx


class GameOver:
    """Event fired when the game is over, including tie games.

    Args:
        was_tie (bool): Whether the game ended in a tie.
        winner (str): The winning side, if any.
    """
    def __init__(self, was_tie: bool = True, winner: str = None):
        self.was_tie = was_tie
        self.winner = winner


class PieceDropEvent:
    """Event fired when a game piece is dropped into an open slot.

    Args:
        side (str): The side that dropped the piece ('red' or 'black').
    """
    def __init__(self, side: str):
        self.side = side

