
"""
Holds the global event bus and the classes holding data for the event messages.
"""

from event_bus import EventBus
bus = EventBus()

mouse_hover_event = "mouse:hover"
mouse_click_event = "mouse:click"
game_undo_event = "game:undo"
game_over_event = "game:over"
game_quit = "game:quit"

piece_drop_event = "piece:drop"


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
