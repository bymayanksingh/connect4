#!/usr/bin/env python3
"""
Parameter sweep for DPAgent on a 3×4 board using linear algebra solution.

Iterates over:
  • gammas   = [0.7, 0.8, 0.9, 0.95]
  • horizons = [2, 3, 4, 5, 6]

Logs:
  |S|   – number of states enumerated
  iter  – policy iteration iterations (where applicable)
  time  – wall-clock runtime
"""

import pathlib
import sys

sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

import itertools
import time

import numpy as np

from connect4.ai.dp_agent import DPAgent
from connect4.ai.game_state import GameState
from connect4.board import GameBoard


def run_one(gamma: float, horizon: int) -> None:
    agent = DPAgent(discount_factor=gamma, use_heuristics=False, use_search=False)

    board = np.zeros((3, 4))
    game_board = GameBoard(rows=3, cols=4)
    root = GameState(board, 0, game_board)

    agent.horizon = horizon

    t0 = time.perf_counter()
    policy, values = agent.solve_game_with_linear_algebra(root, horizon)
    t1 = time.perf_counter()

    num_states = len(agent.all_states)
    iterations = agent.vi_sweeps  # Note: This may be 0 if not using VI
    elapsed = t1 - t0

    print(
        f"γ={gamma:4.2f}  H={horizon:2d}  "
        f"|S|={num_states:4d}  iter={iterations:3d}  "
        f"time={elapsed:6.3f}s"
    )


def main():
    gammas = [0.7, 0.8, 0.9, 0.95]
    horizons = [2, 3, 4, 5, 6]

    print("Parameter sweep (Linear Algebra mode, 3×4 board)")
    for g, h in itertools.product(gammas, horizons):
        run_one(g, h)


if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:
        import os

        devnull = os.open(os.devnull, os.O_WRONLY)
        os.dup2(devnull, sys.stdout.fileno())
        sys.exit(0)
