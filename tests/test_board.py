import pytest
import numpy as np
from connect4.board import GameBoard
from connect4.types import BoardDimensions


def test_board_initialization():
    b = GameBoard(rows=6, cols=7, win_condition=4)
    assert b.rows == 6
    assert b.cols == 7
    assert b.win_condition == 4
    assert b.slots_filled == 0
    assert b.board.shape == (6, 7)
    assert np.all(b.board == 0)
    assert b.dimensions == BoardDimensions(7, 6, 4)


def test_drop_piece_and_open_row(board_7x6):
    b = board_7x6
    assert b.get_next_open_row(0) == 0
    assert b.is_valid_location(0) is True

    b.drop_piece(0, 0, 1)
    assert b.board[0][0] == 1
    assert b.slots_filled == 1
    assert b.get_next_open_row(0) == 1

    b.drop_piece(1, 0, 2)
    assert b.board[1][0] == 2
    assert b.slots_filled == 2
    assert b.get_next_open_row(0) == 2


def test_column_full_validation(board_mini_4x3):
    b = board_mini_4x3  # 3 rows
    col = 1
    assert b.is_valid_location(col) is True

    b.drop_piece(0, col, 1)
    b.drop_piece(1, col, 2)
    b.drop_piece(2, col, 1)

    assert b.is_valid_location(col) is False
    assert b.get_next_open_row(col) is None
    assert col not in b.get_valid_locations()


def test_out_of_bounds_validation(board_7x6):
    b = board_7x6
    assert b.is_valid_location(-1) is False
    assert b.is_valid_location(7) is False
    assert b.is_valid_location(100) is False
    assert b.check_square(1, -1, 0) is False
    assert b.check_square(1, 6, 0) is False
    assert b.check_square(1, 0, 7) is False


def test_undo_move(board_7x6):
    b = board_7x6
    b.drop_piece(0, 3, 1)
    assert b.board[0][3] == 1
    assert b.slots_filled == 1

    b.undo_move(0, 3)
    assert b.board[0][3] == 0
    assert b.slots_filled == 0
    assert b.get_next_open_row(3) == 0


def test_board_copy_independence(board_7x6):
    b = board_7x6
    b.drop_piece(0, 2, 1)

    clone = b.copy()
    assert clone.board[0][2] == 1
    assert clone.slots_filled == 1

    clone.drop_piece(1, 2, 2)
    assert clone.board[1][2] == 2
    assert b.board[1][2] == 0  # original unmodified


def test_board_clear(board_7x6):
    b = board_7x6
    b.drop_piece(0, 0, 1)
    b.drop_piece(0, 1, 2)
    assert b.slots_filled == 2

    b.clear()
    assert b.slots_filled == 0
    assert np.all(b.board == 0)


def test_board_serialization(board_7x6):
    b = board_7x6
    b.drop_piece(0, 3, 1)
    b.drop_piece(1, 3, 2)

    data = b.to_dict()
    assert data["rows"] == 6
    assert data["cols"] == 7
    assert data["slots_filled"] == 2

    restored = GameBoard.from_dict(data)
    assert restored.rows == 6
    assert restored.cols == 7
    assert restored.slots_filled == 2
    assert restored.board[0][3] == 1
    assert restored.board[1][3] == 2
