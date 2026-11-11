import pytest
from connect4.board import GameBoard


def test_horizontal_win(board_7x6):
    b = board_7x6
    # Drop 4 in row 0 for player 1
    for c in range(4):
        b.drop_piece(0, c, 1)

    assert b.horizontal_win(1, 0, 0) is True
    assert b.winning_move(1) is True
    assert b.winning_move(1, 0, 3) is True
    assert b.winning_move(2) is False

    coords = b.get_winning_coordinates(1)
    assert coords == [(0, 0), (0, 1), (0, 2), (0, 3)]


def test_vertical_win(board_7x6):
    b = board_7x6
    # Drop 4 in column 3 for player 2
    for r in range(4):
        b.drop_piece(r, 3, 2)

    assert b.vertical_win(2, 0, 3) is True
    assert b.winning_move(2) is True
    assert b.winning_move(2, 3, 3) is True
    assert b.winning_move(1) is False

    coords = b.get_winning_coordinates(2)
    assert coords == [(0, 3), (1, 3), (2, 3), (3, 3)]


def test_positive_diagonal_win(board_7x6):
    b = board_7x6
    # Create diagonal: (0,0), (1,1), (2,2), (3,3) for player 1
    for i in range(4):
        b.drop_piece(i, i, 1)

    assert b.diagonal_win(1, 0, 0) is True
    assert b.winning_move(1) is True
    assert b.winning_move(1, 3, 3) is True

    coords = b.get_winning_coordinates(1)
    assert coords == [(0, 0), (1, 1), (2, 2), (3, 3)]


def test_negative_diagonal_win(board_7x6):
    b = board_7x6
    # Create diagonal: (3,0), (2,1), (1,2), (0,3) for player 2
    for i in range(4):
        b.drop_piece(3 - i, i, 2)

    assert b.diagonal_win(2, 3, 0) is True
    assert b.winning_move(2) is True
    assert b.winning_move(2, 0, 3) is True

    coords = b.get_winning_coordinates(2)
    assert coords == [(3, 0), (2, 1), (1, 2), (0, 3)]


def test_tie_condition():
    # 2x2 board, connect 3 -> no one can win, tie when filled
    b = GameBoard(rows=2, cols=2, win_condition=3)
    b.drop_piece(0, 0, 1)
    b.drop_piece(0, 1, 2)
    b.drop_piece(1, 0, 2)
    assert b.tie_move() is False

    b.drop_piece(1, 1, 1)
    assert b.is_full() is True
    assert b.tie_move() is True


def test_connect_3_generalized(board_mini_4x3):
    b = board_mini_4x3  # 4 cols, 3 rows, connect 3
    b.drop_piece(0, 0, 1)
    b.drop_piece(0, 1, 1)
    assert b.winning_move(1) is False

    b.drop_piece(0, 2, 1)
    assert b.winning_move(1) is True
    assert b.get_winning_coordinates(1) == [(0, 0), (0, 1), (0, 2)]
