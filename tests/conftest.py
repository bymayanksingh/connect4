import os
import pytest
import numpy as np

# Ensure Pygame runs headless during testing
os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

from connect4.board import GameBoard
from connect4.game import Connect4Game
from connect4.types import BoardDimensions, GameMode, Player


@pytest.fixture
def board_7x6():
    return GameBoard(rows=6, cols=7, win_condition=4)


@pytest.fixture
def board_mini_4x3():
    return GameBoard(rows=3, cols=4, win_condition=3)


@pytest.fixture
def pvp_game():
    return Connect4Game(mode=GameMode.PVP)
