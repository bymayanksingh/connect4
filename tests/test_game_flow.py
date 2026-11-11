import pytest
from connect4.game import Connect4Game
from connect4.types import GameMode, GameStatus, Player


def test_game_turn_progression(pvp_game):
    game = pvp_game
    assert game.current_player == Player.P1
    assert game.turn == 0

    res1 = game.make_move(3)
    assert res1.player == Player.P1
    assert res1.row == 0
    assert res1.col == 3
    assert game.current_player == Player.P2
    assert game.turn == 1

    res2 = game.make_move(3)
    assert res2.player == Player.P2
    assert res2.row == 1
    assert res2.col == 3
    assert game.current_player == Player.P1


def test_game_undo_redo(pvp_game):
    game = pvp_game
    game.make_move(0)  # P1
    game.make_move(1)  # P2
    assert len(game.move_history) == 2
    assert game.board.slots_filled == 2

    undone = game.undo()
    assert undone.col == 1
    assert undone.player == Player.P2
    assert len(game.move_history) == 1
    assert game.current_player == Player.P2
    assert game.board.slots_filled == 1

    redone = game.redo()
    assert redone.col == 1
    assert redone.player == Player.P2
    assert len(game.move_history) == 2
    assert game.current_player == Player.P1


def test_game_winning_move_locks_session(pvp_game):
    game = pvp_game
    # Play 3 moves each in cols 0 and 1
    for _ in range(3):
        game.make_move(0)  # P1
        game.make_move(1)  # P2

    # P1 plays winning 4th move in col 0
    win_res = game.make_move(0)
    assert win_res.is_win is True
    assert game.status == GameStatus.WIN_P1
    assert game.is_game_over is True
    assert game.winner == Player.P1

    # Attempting to move after win raises RuntimeError
    with pytest.raises(RuntimeError):
        game.make_move(2)


def test_game_restart(pvp_game):
    game = pvp_game
    game.make_move(0)
    game.make_move(1)
    assert game.board.slots_filled == 2

    game.restart()
    assert game.board.slots_filled == 0
    assert game.current_player == Player.P1
    assert game.status == GameStatus.IN_PROGRESS
    assert len(game.move_history) == 0


def test_game_serialization(pvp_game):
    game = pvp_game
    game.make_move(3)
    d = game.to_dict()
    assert d["current_player"] == 2
    assert d["turn"] == 1
    assert d["status"] == "in_progress"
    assert d["total_moves"] == 1
