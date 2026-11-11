from __future__ import annotations

import io
from pathlib import Path
from typing import List, Optional, Tuple, Union
import numpy as np

from connect4.board import GameBoard
from connect4.types import Player


class Visualizer:
    """
    Headless visualization and diagram generation pipeline.
    Exports board state to ASCII, SVG vector art, and Graphviz DOT graph format.
    """

    @staticmethod
    def to_ascii(
        board: GameBoard,
        winning_coords: Optional[List[Tuple[int, int]]] = None,
        use_unicode: bool = True,
    ) -> str:
        """
        Renders the board as formatted ASCII/Unicode text.
        """
        p1_char = "🔴" if use_unicode else "X"
        p2_char = "🟡" if use_unicode else "O"
        win_p1 = "⭐" if use_unicode else "*"
        win_p2 = "🌟" if use_unicode else "#"
        empty_char = "⚪" if use_unicode else "."

        win_set = set(winning_coords or [])

        lines = []
        lines.append("╔" + "═══╦" * (board.cols - 1) + "═══╗")

        for r in range(board.rows - 1, -1, -1):
            row_str = "║"
            for c in range(board.cols):
                val = board.board[r][c]
                is_win = (r, c) in win_set

                if val == 1:
                    cell = win_p1 if is_win else p1_char
                elif val == 2:
                    cell = win_p2 if is_win else p2_char
                else:
                    cell = empty_char

                row_str += f" {cell} ║"
            lines.append(row_str)
            if r > 0:
                lines.append("╠" + "═══╬" * (board.cols - 1) + "═══╣")

        lines.append("╚" + "═══╩" * (board.cols - 1) + "═══╝")
        col_headers = "  " + "   ".join(str(c + 1) for c in range(board.cols))
        lines.append(col_headers)
        return "\n".join(lines)

    @staticmethod
    def to_svg(
        board: GameBoard,
        cell_size: int = 60,
        margin: int = 20,
        winning_coords: Optional[List[Tuple[int, int]]] = None,
    ) -> str:
        """
        Generates a standalone, clean vector SVG string representing the Connect 4 board.
        """
        width = board.cols * cell_size + 2 * margin
        height = board.rows * cell_size + 2 * margin + 40
        radius = int(cell_size * 0.4)

        win_set = set(winning_coords or [])

        svg_parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
            f'width="{width}" height="{height}">',
            '  <defs>',
            '    <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">',
            '      <feDropShadow dx="2" dy="2" stdDeviation="3" flood-opacity="0.3"/>',
            '    </filter>',
            '  </defs>',
            '  <!-- Background -->',
            f'  <rect width="{width}" height="{height}" fill="#1A202C" rx="10"/>',
            '  <!-- Blue Board Frame -->',
            f'  <rect x="{margin}" y="{margin}" width="{board.cols * cell_size}" '
            f'height="{board.rows * cell_size}" rx="12" fill="#1E40AF" filter="url(#shadow)"/>',
        ]

        # Draw grid slots
        for r in range(board.rows):
            # In SVG, y=0 is top, so row 0 (bottom of Connect4) is at max Y
            svg_y = margin + (board.rows - 1 - r) * cell_size + cell_size // 2
            for c in range(board.cols):
                svg_x = margin + c * cell_size + cell_size // 2
                val = board.board[r][c]
                is_win = (r, c) in win_set

                if val == 1:
                    fill = "#EF4444"  # Red
                    stroke = "#FCD34D" if is_win else "#B91C1C"
                    stroke_w = "4" if is_win else "1"
                elif val == 2:
                    fill = "#FBBF24"  # Yellow
                    stroke = "#FFFFFF" if is_win else "#D97706"
                    stroke_w = "4" if is_win else "1"
                else:
                    fill = "#0F172A"  # Empty slot
                    stroke = "#1E293B"
                    stroke_w = "1"

                svg_parts.append(
                    f'  <circle cx="{svg_x}" cy="{svg_y}" r="{radius}" '
                    f'fill="{fill}" stroke="{stroke}" stroke-width="{stroke_w}"/>'
                )

        # Column indicators at bottom
        for c in range(board.cols):
            svg_x = margin + c * cell_size + cell_size // 2
            svg_y = margin + board.rows * cell_size + 25
            svg_parts.append(
                f'  <text x="{svg_x}" y="{svg_y}" font-family="sans-serif" font-size="14" '
                f'font-weight="bold" fill="#94A3B8" text-anchor="middle">{c + 1}</text>'
            )

        svg_parts.append('</svg>')
        return "\n".join(svg_parts)

    @staticmethod
    def to_dot(
        board: GameBoard,
        title: str = "ConnectFour",
        winning_coords: Optional[List[Tuple[int, int]]] = None,
    ) -> str:
        """
        Generates Graphviz DOT graph language definition.
        """
        win_set = set(winning_coords or [])
        lines = [
            f'digraph {title} {{',
            '  rankdir=TB;',
            '  node [shape=circle, width=0.6, fixedsize=true, fontname="Helvetica"];',
            '  edge [style=invis];',
            '  compound=true;',
        ]

        # Define grid nodes
        for r in range(board.rows - 1, -1, -1):
            row_nodes = []
            for c in range(board.cols):
                node_id = f"cell_{r}_{c}"
                val = board.board[r][c]
                is_win = (r, c) in win_set

                if val == 1:
                    fill = "#EF4444"
                    font = "white"
                    label = "P1"
                elif val == 2:
                    fill = "#FBBF24"
                    font = "black"
                    label = "P2"
                else:
                    fill = "#E2E8F0"
                    font = "gray"
                    label = ""

                border = 'penwidth=3.0, color="#10B981"' if is_win else 'penwidth=1.0'
                lines.append(
                    f'  {node_id} [label="{label}", style=filled, fillcolor="{fill}", '
                    f'fontcolor="{font}", {border}];'
                )
                row_nodes.append(node_id)

            # Keep row nodes on same rank
            lines.append(f'  {{ rank=same; {" ".join(row_nodes)} }}')

        # Vertical edges to maintain grid ordering
        for c in range(board.cols):
            for r in range(board.rows - 1, 0, -1):
                lines.append(f"  cell_{r}_{c} -> cell_{r-1}_{c};")

        lines.append('}')
        return "\n".join(lines)

    @classmethod
    def save_svg(
        cls,
        board: GameBoard,
        path: Union[str, Path],
        cell_size: int = 60,
        margin: int = 20,
        winning_coords: Optional[List[Tuple[int, int]]] = None,
    ) -> None:
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(cls.to_svg(board, cell_size=cell_size, margin=margin, winning_coords=winning_coords))

    @classmethod
    def save_dot(
        cls,
        board: GameBoard,
        path: Union[str, Path],
        title: str = "ConnectFour",
        winning_coords: Optional[List[Tuple[int, int]]] = None,
    ) -> None:
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(cls.to_dot(board, title=title, winning_coords=winning_coords))
