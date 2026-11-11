from __future__ import annotations

import argparse
import json
import sys
import time
from typing import List, Optional

from connect4.ai.factory import AgentFactory
from connect4.board import GameBoard
from connect4.game import Connect4Game
from connect4.types import BoardDimensions, GameMode, GameStatus, Player
from connect4.visualizer.export import Visualizer


def play_terminal_interactive(
    game: Connect4Game,
    use_unicode: bool = True,
    export_svg_path: Optional[str] = None,
    export_dot_path: Optional[str] = None,
) -> None:
    """Runs an interactive turn-based Connect 4 session directly in the terminal."""
    print("\n" + "=" * 50)
    print("           WELCOME TO CONNECT FOUR")
    print("=" * 50)
    print(f"Board: {game.board.cols}x{game.board.rows} (Connect {game.board.win_condition})")
    print(f"Mode:  {game.mode.value.upper()}")
    print("Commands: Enter column number (1..{0}), 'u' (undo), 'r' (restart), 'q' (quit)\n".format(game.board.cols))

    while not game.is_game_over:
        print(Visualizer.to_ascii(game.board, use_unicode=use_unicode))
        print()

        current_agent = game.get_current_agent()
        if current_agent:
            print(f"🤖 {current_agent.name} is thinking...")
            t0 = time.perf_counter()
            result = game.play_ai_turn()
            t1 = time.perf_counter()
            if result:
                print(f"🤖 {current_agent.name} played Column {result.col + 1} ({t1 - t0:.3f}s)")
            continue

        player_name = game.current_player.display_name
        try:
            raw_input = input(f"{player_name} > ").strip().lower()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting game.")
            sys.exit(0)

        if not raw_input:
            continue

        # Check command aliases
        if raw_input in ("q", "quit", "exit"):
            print("Game aborted.")
            return
        elif raw_input in ("u", "undo"):
            undone = game.undo()
            if undone:
                print(f"Undid move at column {undone.col + 1}.")
                # If playing against AI, undo the AI move as well
                if game.mode == GameMode.PVA:
                    game.undo()
            else:
                print("No moves to undo.")
            continue
        elif raw_input in ("r", "restart", "reset"):
            game.restart()
            print("Game restarted.")
            continue
        elif raw_input in ("h", "help", "?"):
            print("Help: Enter column 1 to {0}, or type 'undo', 'restart', 'quit'.".format(game.board.cols))
            continue

        # Parse column
        try:
            col_1based = int(raw_input)
            col_0based = col_1based - 1
            if col_0based < 0 or col_0based >= game.board.cols:
                print(f"Invalid column! Please enter a number between 1 and {game.board.cols}.")
                continue
            if not game.board.is_valid_location(col_0based):
                print(f"Column {col_1based} is completely full! Choose another column.")
                continue

            game.make_move(col_0based)
        except ValueError:
            print(f"Unrecognized input '{raw_input}'. Type a column number (1..{game.board.cols}) or 'help'.")

    # Game Over summary
    print("\n" + "=" * 50)
    print("                    GAME OVER")
    print("=" * 50)
    winning_coords = game.board.get_winning_coordinates(int(game.winner)) if game.winner else None
    print(Visualizer.to_ascii(game.board, winning_coords=winning_coords, use_unicode=use_unicode))
    print()

    if game.status == GameStatus.DRAW:
        print("🤝 It's a DRAW! The board is full.")
    else:
        winner_name = game.winner.display_name if game.winner else "Unknown"
        print(f"🏆 {winner_name} WINS THE GAME!")

    if export_svg_path:
        Visualizer.save_svg(game.board, export_svg_path)
        print(f"Vector SVG board exported to: {export_svg_path}")

    if export_dot_path:
        Visualizer.save_dot(game.board, export_dot_path)
        print(f"Graphviz DOT diagram exported to: {export_dot_path}")


def run_benchmark(
    ai1_name: str,
    ai2_name: str,
    num_games: int = 10,
    dimensions: Optional[BoardDimensions] = None,
) -> None:
    """Runs automated headless matches between two AI agents and reports statistics."""
    dims = dimensions or BoardDimensions()
    agent1 = AgentFactory.create_agent(ai1_name, name=f"P1 ({ai1_name})")
    agent2 = AgentFactory.create_agent(ai2_name, name=f"P2 ({ai2_name})")

    print("\n" + "=" * 60)
    print("         CONNECT 4 HEADLESS BENCHMARK TOURNAMENT")
    print("=" * 60)
    print(f"Agent 1 (Player 1 - Red):    {agent1.name}")
    print(f"Agent 2 (Player 2 - Yellow): {agent2.name}")
    print(f"Board size:                  {dims.cols}x{dims.rows} (Connect {dims.win_condition})")
    print(f"Matches scheduled:           {num_games}")
    print("-" * 60)

    p1_wins = 0
    p2_wins = 0
    draws = 0
    total_moves = 0
    start_time = time.perf_counter()

    for game_idx in range(1, num_games + 1):
        game = Connect4Game(dimensions=dims, mode=GameMode.AVA, agent1=agent1, agent2=agent2)
        match_start = time.perf_counter()

        while not game.is_game_over:
            game.play_ai_turn()

        elapsed = time.perf_counter() - match_start
        total_moves += len(game.move_history)

        if game.status == GameStatus.WIN_P1:
            p1_wins += 1
            res = "P1 WIN "
        elif game.status == GameStatus.WIN_P2:
            p2_wins += 1
            res = "P2 WIN "
        else:
            draws += 1
            res = "DRAW   "

        print(f"Game {game_idx:2d}/{num_games}: {res} in {len(game.move_history):2d} moves ({elapsed:.3f}s)")

    total_time = time.perf_counter() - start_time
    print("-" * 60)
    print("                     FINAL RESULTS")
    print("-" * 60)
    print(f"Agent 1 ({ai1_name}) Wins: {p1_wins} ({p1_wins / num_games * 100:.1f}%)")
    print(f"Agent 2 ({ai2_name}) Wins: {p2_wins} ({p2_wins / num_games * 100:.1f}%)")
    print(f"Draws:                   {draws} ({draws / num_games * 100:.1f}%)")
    print(f"Avg Moves per Match:     {total_moves / num_games:.1f}")
    print(f"Total Wall-Clock Time:   {total_time:.3f}s ({total_time / num_games:.3f}s/game)")
    print("=" * 60 + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="connect4",
        description="Connect 4: Production-Grade Game, AI Engine & Visualizer",
    )
    parser.add_argument(
        "--gui", action="store_true", help="Launch the graphical Pygame interface"
    )
    parser.add_argument(
        "--mode",
        choices=["pvp", "pva", "ava"],
        default="pva",
        help="Game mode: pvp (Player vs Player), pva (Player vs AI), ava (AI vs AI)",
    )
    parser.add_argument(
        "--ai",
        choices=AgentFactory.available_agents(),
        default="medium",
        help="AI agent algorithm for Player vs AI mode (default: medium)",
    )
    parser.add_argument(
        "--ai1",
        choices=AgentFactory.available_agents(),
        default="hard",
        help="Player 1 AI algorithm for AI vs AI / benchmark mode",
    )
    parser.add_argument(
        "--ai2",
        choices=AgentFactory.available_agents(),
        default="easy",
        help="Player 2 AI algorithm for AI vs AI / benchmark mode",
    )
    parser.add_argument(
        "--benchmark",
        action="store_true",
        help="Run an automated headless tournament between --ai1 and --ai2",
    )
    parser.add_argument(
        "-n", "--games", type=int, default=5, help="Number of benchmark games to run"
    )
    parser.add_argument(
        "--rows", type=int, default=6, help="Grid rows (default: 6)"
    )
    parser.add_argument(
        "--cols", type=int, default=7, help="Grid columns (default: 7)"
    )
    parser.add_argument(
        "--connect", type=int, default=4, help="Consecutive chips to win (default: 4)"
    )
    parser.add_argument(
        "--json", action="store_true", help="Output initial or benchmark state as JSON"
    )
    parser.add_argument(
        "--export-svg", type=str, default=None, help="Save final board state as SVG image"
    )
    parser.add_argument(
        "--export-dot", type=str, default=None, help="Save final board state as Graphviz DOT"
    )
    parser.add_argument(
        "--no-unicode", action="store_true", help="Use standard ASCII characters instead of emoji"
    )

    args = parser.parse_args()
    dims = BoardDimensions(cols=args.cols, rows=args.rows, win_condition=args.connect)

    if args.gui:
        try:
            from connect4.gui.app import run_gui
            run_gui()
            return
        except ImportError as e:
            print(f"Error launching GUI: {e}")
            sys.exit(1)

    if args.benchmark:
        run_benchmark(ai1_name=args.ai1, ai2_name=args.ai2, num_games=args.games, dimensions=dims)
        return

    # Setup terminal interactive mode
    mode = GameMode(args.mode)
    agent1 = None
    agent2 = None

    if mode == GameMode.PVA:
        agent2 = AgentFactory.create_agent(args.ai, name=f"AI ({args.ai.title()})")
    elif mode == GameMode.AVA:
        agent1 = AgentFactory.create_agent(args.ai1, name=f"P1 ({args.ai1.title()})")
        agent2 = AgentFactory.create_agent(args.ai2, name=f"P2 ({args.ai2.title()})")

    game = Connect4Game(dimensions=dims, mode=mode, agent1=agent1, agent2=agent2)

    if args.json:
        print(json.dumps(game.to_dict(), indent=2))
        return

    play_terminal_interactive(
        game=game,
        use_unicode=not args.no_unicode,
        export_svg_path=args.export_svg,
        export_dot_path=args.export_dot,
    )


if __name__ == "__main__":
    main()
