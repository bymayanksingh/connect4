#!/usr/bin/env python3
"""
AI Tournament Benchmark Runner.
Executes head-to-head matches between any two AI engines across configurable board sizes.
"""
import argparse
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from connect4.cli import run_benchmark
from connect4.types import BoardDimensions
from connect4.ai.factory import AgentFactory


def main():
    parser = argparse.ArgumentParser(description="Connect 4 AI Tournament Benchmark")
    parser.add_argument("--p1", default="hard", choices=AgentFactory.available_agents(), help="Player 1 AI")
    parser.add_argument("--p2", default="medium", choices=AgentFactory.available_agents(), help="Player 2 AI")
    parser.add_argument("-n", "--games", type=int, default=10, help="Number of games to simulate")
    parser.add_argument("--rows", type=int, default=6, help="Rows")
    parser.add_argument("--cols", type=int, default=7, help="Columns")
    parser.add_argument("--connect", type=int, default=4, help="Win condition length")

    args = parser.parse_args()
    dims = BoardDimensions(cols=args.cols, rows=args.rows, win_condition=args.connect)
    run_benchmark(ai1_name=args.p1, ai2_name=args.p2, num_games=args.games, dimensions=dims)


if __name__ == "__main__":
    main()
