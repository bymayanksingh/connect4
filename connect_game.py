import math
import os
import sys

import pygame

from config import black
from events import GameOver, MouseClickEvent, PieceDropEvent, bus
from game_data import GameData
from game_renderer import GameRenderer

from typing import List
from agents import Agent


class ConnectGame:
    """
    Holds all of the game logic and game data.
    """

    game_data: GameData
    renderer: GameRenderer

    def __init__(self, game_data: GameData, renderer: GameRenderer):
        """
        Initializes the connect game.
        :param game_data: A reference to the game data object.
        :param renderer: A reference to the game renderer.
        """
        self.game_data = game_data
        self.renderer = renderer

    def quit(self):
        """
        Exits the game.
        """
        sys.exit()

    @bus.on("mouse:click")
    def mouse_click(self, event: MouseClickEvent):
        """
        Handles a mouse click event.
        :param event: Data about the mouse click
        """
        pygame.draw.rect(
            self.renderer.screen,
            black,
            (0, 0, self.game_data.width, self.game_data.sq_size),
        )

        col: int = int(math.floor(event.posx / self.game_data.sq_size))

        self.do_movement(col)

    @bus.on("game:undo")
    def undo(self):
        """
        Handles the Ctrl+Z keyboard sequence, which
        is used to roll back the last move.
        :return:
        """
        if self.game_data.last_move_row:

            self.game_data.last_move_row.pop()
            self.game_data.last_move_col.pop()

            self.game_data.game_board.slots_filled -= 1
            self.game_data.turn += 1
            self.game_data.turn = self.game_data.turn % 2

    def do_movement(self, col: int):
        """
        Inserts a new piece in the specified column and prints the new board
        """
        if self.game_data.game_board.is_valid_location(col):
            row: int = self.game_data.game_board.get_next_open_row(col)

            self.game_data.last_move_row.append(row)
            self.game_data.last_move_col.append(col)
            self.game_data.game_board.drop_piece(row, col, self.game_data.turn + 1)

            self.draw()

            bus.emit(
                "piece:drop", PieceDropEvent(self.game_data.game_board.board[row][col])
            )

            self.print_board()

            if self.game_data.game_board.winning_move(self.game_data.turn + 1, row, col):
                bus.emit(
                    "game:over", self.renderer, GameOver(False, self.game_data.turn + 1)
                )
                self.game_data.game_over = True

            pygame.display.update()

            self.game_data.turn += 1
            self.game_data.turn = self.game_data.turn % 2

    @staticmethod
    def compare_agents(agent1: Agent, agent2: Agent, n=100, alternate=True) -> List[int]:
        """
        :param agent1: an AI agent
        :param agent2: an AI agent
        :param n: number of matches
        :param alternate: if True agent1 and agent2 will play first the same number of times
        :returns: number of [ties, agent1 wins, agent2 wins]
        """

        def play_game(agent1: Agent, agent2: Agent) -> int:
            """
            Agent1 plays first, agent2 plays second
            :param agent1: an AI agent
            :param agent2: an AI agent
            :returns: the winner; 1 = agent1, 2 = agent2, 0 = tie
            """
            data = GameData()
            board = data.game_board
            while True:
                col = agent1.get_move(data)
                row = board.get_next_open_row(col)
                board.drop_piece(row, col, 1)
                if board.winning_move(1, row, col):
                    return 1

                data.turn += 1
                data.turn = data.turn % 2

                col = agent2.get_move(data)
                row = board.get_next_open_row(col)
                board.drop_piece(row, col, 2)

                if board.winning_move(2, row, col):
                    return 2

                if board.tie_move():
                    return 0

        stats = [0, 0, 0]
        if alternate:
            for _ in range(n // 2):
                winner = play_game(agent1, agent2)
                stats[winner] += 1

                winner = play_game(agent2, agent1)
                if winner == 1:
                    stats[2] += 1
                elif winner == 2:
                    stats[1] += 1
                else:
                    stats[0] += 1
        else:
            for _ in range(n):
                winner = play_game(agent1, agent2)
                stats[winner] += 1

        return stats

    def update(self):
        """
        Checks the game state, dispatching events as needed.
        """
        if self.game_data.game_board.tie_move():
            bus.emit("game:over", self.renderer, GameOver(was_tie=True))

            self.game_data.game_over = True

        if self.game_data.game_over:
            print(os.getpid())
            pygame.time.wait(1000)
            os.system("game.py")

    def draw(self):
        """
        Directs the game renderer to 'render' the game state to the audio and video devices.
        """
        self.renderer.draw(self.game_data)

    def print_board(self):
        """
        Prints the state of the board to the console.
        """
        self.game_data.game_board.print_board()
