import pytest
from connect4.ai.heuristic_agent import HeuristicAgent
from connect4.ai.minimax import MinimaxAgent
from connect4.ai.random_agent import RandomAgent
from connect4.ai.dp_agent import DPAgent
from connect4.board import GameBoard
from connect4.game import Connect4Game
from connect4.types import GameMode, Player


def test_random_agent_valid_move(board_7x6):
    agent = RandomAgent()
    move = agent.get_move(board_7x6, Player.P1)
    assert 0 <= move < board_7x6.cols
    assert board_7x6.is_valid_location(move)


def test_heuristic_agent_takes_immediate_win(board_7x6):
    agent = HeuristicAgent()
    # P1 has 3 in row 0 at cols 0, 1, 2
    board_7x6.drop_piece(0, 0, 1)
    board_7x6.drop_piece(0, 1, 1)
    board_7x6.drop_piece(0, 2, 1)

    move = agent.get_move(board_7x6, Player.P1)
    # Must choose col 3 to complete 4-in-a-row
    assert move == 3


def test_heuristic_agent_blocks_opponent_win(board_7x6):
    agent = HeuristicAgent()
    # Opponent (P1) has 3 in col 2: rows 0, 1, 2
    board_7x6.drop_piece(0, 2, 1)
    board_7x6.drop_piece(1, 2, 1)
    board_7x6.drop_piece(2, 2, 1)

    # Agent is playing as P2
    move = agent.get_move(board_7x6, Player.P2)
    # Must drop in col 2 to block P1's vertical win
    assert move == 2


def test_minimax_agent_takes_winning_move(board_7x6):
    agent = MinimaxAgent(depth=3)
    board_7x6.drop_piece(0, 3, 2)
    board_7x6.drop_piece(0, 4, 2)
    board_7x6.drop_piece(0, 5, 2)

    move = agent.get_move(board_7x6, Player.P2)
    # Either col 2 or col 6 wins
    assert move in (2, 6)


def test_minimax_agent_opening_move_takes_center(board_7x6):
    agent = MinimaxAgent(depth=3)
    # Empty 7-col board: center is 3
    move = agent.get_move(board_7x6, Player.P1)
    assert move == 3


def test_dp_agent_valid_move():
    agent = DPAgent(horizon=2, verbose=False)
    b = GameBoard(rows=3, cols=4, win_condition=3)
    move = agent.get_move(b, Player.P1)
    assert 0 <= move < b.cols
    assert b.is_valid_location(move)
