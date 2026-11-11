"""
Backward compatibility layer for legacy game_data.py.
For modern development, import directly from connect4.
"""
from connect4.board import GameBoard
from connect4.types import BoardDimensions

class GameData:
    """Legacy GameData representation."""
    def __init__(self):
        self.cols = 7
        self.rows = 6
        self.win_condition = 4
        self.sq_size = 100
        self.game_board = GameBoard(self.rows, self.cols, self.win_condition)
        self.turn = 0
        self.game_over = False
        self.last_move_row = []
        self.last_move_col = []
        self.game_mode = 'pvp'
        self.agent1 = None
        self.agent2 = None

    @property
    def width(self) -> int:
        return self.cols * self.sq_size

    @property
    def height(self) -> int:
        return (self.rows + 1) * self.sq_size

    @property
    def size(self) -> tuple:
        return (self.width, self.height)

    def set_board_size(self, cols: int, rows: int, win_condition: int = 4):
        self.cols = cols
        self.rows = rows
        self.win_condition = win_condition
        self.game_board = GameBoard(rows, cols, win_condition)

    def set_game_mode(self, mode: str):
        self.game_mode = mode

    def get_state_for_agent(self) -> dict:
        return {
            "board": self.game_board.board,
            "turn": self.turn,
            "game_board": self.game_board
        }

__all__ = ["GameData"]
