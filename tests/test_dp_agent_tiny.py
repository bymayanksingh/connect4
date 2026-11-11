import numpy as np

from connect4.ai.dp_agent import DPAgent
from connect4.ai.game_state import GameState
from connect4.board import GameBoard


def test_dp_agent_linear_algebra_solve():
    """Verifies that the DP linear algebra transition solver computes policy on a small board."""
    agent = DPAgent(discount_factor=0.9, use_heuristics=False, use_search=False, verbose=False)
    game_board = GameBoard(rows=2, cols=3, win_condition=3)
    root = GameState(np.zeros((2, 3), dtype=int), 0, game_board)
    policy, values = agent.solve_game_with_linear_algebra(root, horizon=2)
    assert isinstance(policy, dict)
    assert isinstance(values, dict)
    assert len(values) > 0
