#!/usr/bin/env python3
"""
CLI Diagram Exporter.
Exports current board state to SVG, Graphviz DOT, or ASCII diagram.
"""
import argparse
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from connect4.board import GameBoard
from connect4.visualizer.export import Visualizer


def main():
    parser = argparse.ArgumentParser(description="Export Connect 4 diagrams")
    parser.add_argument("--svg", type=str, default="docs/board.svg", help="Path to save SVG")
    parser.add_argument("--dot", type=str, default="docs/board.dot", help="Path to save DOT")
    parser.add_argument("--rows", type=int, default=6)
    parser.add_argument("--cols", type=int, default=7)

    args = parser.parse_args()
    b = GameBoard(rows=args.rows, cols=args.cols)

    # Place a few sample pieces for illustrative diagram
    sample_moves = [(0, 3, 1), (0, 2, 2), (1, 3, 1), (0, 4, 2), (2, 3, 1), (0, 1, 2), (3, 3, 1)]
    for r, c, p in sample_moves:
        b.drop_piece(r, c, p)

    winning_coords = b.get_winning_coordinates(1)

    if args.svg:
        Visualizer.save_svg(b, args.svg, winning_coords=winning_coords)
        print(f"Exported SVG diagram to {args.svg}")

    if args.dot:
        Visualizer.save_dot(b, args.dot, winning_coords=winning_coords)
        print(f"Exported Graphviz DOT diagram to {args.dot}")


if __name__ == "__main__":
    main()
