import pytest
from connect4.cli import run_benchmark
from connect4.types import BoardDimensions


def test_cli_benchmark_execution(capsys):
    # Run a quick 2-game benchmark between Hard and Easy on mini board
    dims = BoardDimensions(cols=4, rows=3, win_condition=3)
    run_benchmark(ai1_name="hard", ai2_name="easy", num_games=2, dimensions=dims)

    captured = capsys.readouterr()
    assert "CONNECT 4 HEADLESS BENCHMARK TOURNAMENT" in captured.out
    assert "FINAL RESULTS" in captured.out
    assert "Matches scheduled:           2" in captured.out
