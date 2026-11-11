"""
Backward compatibility layer for legacy connect_game.py.
For modern development, import directly from connect4.
"""
from connect4.game import Connect4Game
from connect4.gui.renderer import GameRenderer
from connect4.events import bus, MouseClickEvent, PieceDropEvent, GameOver

class ConnectGame:
    """Legacy ConnectGame wrapper around Connect4Game."""
    def __init__(self, game_data, renderer: GameRenderer):
        self.game_data = game_data
        self.renderer = renderer
        self._game = Connect4Game(board=game_data.game_board)

    def quit(self):
        import sys
        sys.exit(0)

    def draw(self):
        if self.renderer:
            self.renderer.draw_board(self._game)

    def print_board(self):
        self._game.board.print_board()

    def update(self):
        if self._game.board.tie_move():
            bus.emit("game:over", self.renderer, GameOver(was_tie=True))
            self.game_data.game_over = True

    def make_move(self, col: int, is_agent_move: bool = False):
        try:
            res = self._game.make_move(col)
            self.game_data.turn = self._game.turn
            self.game_data.game_over = self._game.is_game_over
            return True
        except (ValueError, RuntimeError):
            return False

__all__ = ["ConnectGame", "Connect4Game"]
