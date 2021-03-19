from random import choice
from copy import deepcopy
from game_data import GameData
import abc


class Agent(abc.ABC):
    """
    It is an abstract class. All the agents must inherit from this class.
    """

    def get_move(self, game_data: GameData) -> int:
        pass


class RandomAgent(Agent):
    """
    An agent which makes random moves.
    """

    @staticmethod
    def get_move(data) -> int:
        """ returns a random valid col"""
        return choice([c for c in range(7) if data.game_board.is_valid_location(c)])


class MinimaxAgent(Agent):
    """
    An agent designed to play connect-4 in a 6x7 board.
    It uses the minimax algorithm and alpha-beta pruning with a recommend depth of 5 moves.
    The heuristic it is based on the Odd-Even strategy and it is 100% original.
    """
    __depth: int

    def __init__(self, depth=5):
        self.__depth = depth

    @staticmethod
    def get_board_value(game_data: GameData) -> int:

        """
        We calculate this value with the following heuristic:
        - Squares value:
            [[0 0 0 0 0 0 0]
             [0 0 1 2 1 0 0]
             [0 0 1 2 1 0 0]
             [0 0 2 2 2 0 0]
             [0 0 2 2 2 0 0]
             [0 0 0 2 0 0 0]]

        - We also take into account the win squares of each player and where they are located.
        This heuristic is mainly based on the Odd-Even strategy.
        More info about this strategy in: https://www.youtube.com/watch?v=YqqcNjQMX18

        :param game_data: All of the data for the game.
        :returns: The value of the board. Positive positions are good for player 1
        while negative ones indicate a better position for player 2.
        """
        if game_data.game_board.slots_filled == 0:
            return 0

        if game_data.winner == 1:
            return 1000
        elif game_data.winner == 2:
            return -1000

        total_value = 0

        # Setting points per piece position:
        for row in game_data.game_board.board[3:5, 2:5:2]:
            for chip in row:
                if chip == 1:
                    total_value += 1
                elif chip == 2:
                    total_value -= 1

        for row in game_data.game_board.board[1:3, 2:5:2]:
            for chip in row:
                if chip == 1:
                    total_value += 2
                elif chip == 2:
                    total_value -= 2

        for chip in game_data.game_board.board[:5, 3]:
            if chip == 1:
                total_value += 2
            elif chip == 2:
                total_value -= 2

        # Setting points per win square (Odd-Even strategy):
        p1_win_odd_rows_per_column = \
            [[r for r, c in game_data.game_board.p1_win_squares if c == i and r % 2 == 0] for i in range(7)]
        p2_win_odd_rows_per_column = \
            [[r for r, c in game_data.game_board.p2_win_squares if c == i and r % 2 == 0] for i in range(7)]

        p1_win_even_rows_per_column = \
            [[r for r, c in game_data.game_board.p1_win_squares if c == i and r % 2 == 1] for i in range(7)]
        p2_win_even_rows_per_column = \
            [[r for r, c in game_data.game_board.p2_win_squares if c == i and r % 2 == 1] for i in range(7)]

        for c in range(7):
            # Column winners:
            p1_best_even_row = 10 if not p1_win_even_rows_per_column[c] else min(p1_win_even_rows_per_column[c])
            p2_best_even_row = 10 if not p2_win_even_rows_per_column[c] else min(p2_win_even_rows_per_column[c])

            p2_best_odd_row = 10 if not p2_win_odd_rows_per_column[c] else min(p2_win_odd_rows_per_column[c])
            p1_best_odd_row = 10 if not p1_win_odd_rows_per_column[c] else min(p1_win_odd_rows_per_column[c])

            if p1_best_odd_row < p2_best_even_row:
                total_value += 100 - p1_best_odd_row * 5

            if p2_best_odd_row < p1_best_even_row:
                total_value -= 10 - p2_best_odd_row

            if p2_best_even_row < p1_best_odd_row:
                total_value -= 50 - p2_best_even_row * 3

        return total_value

    @staticmethod
    def __drop_piece(data, row, col, piece):
        """
        Drops a piece (it should be in a copy board, not in the original data)
        and updates all the necessary information.
        """
        data.game_board.drop_piece(row, col, piece)
        data.turn += 1
        data.turn %= 2
        if data.game_board.winning_move(piece, row, col):
            data.game_over = True
            data.winner = piece

    @staticmethod
    def _alpha_beta(data: GameData, col: int, depth=5, alpha=-1001, beta=1001) -> int:
        """
        :return: The value of a given movement.
        """

        # making the move in a copy of the real board:
        data_copy = deepcopy(data)
        piece = data_copy.turn + 1
        row = data_copy.game_board.get_next_open_row(col)
        MinimaxAgent.__drop_piece(data_copy, row, col, piece)

        if depth == 0 or data_copy.game_over:
            return MinimaxAgent.get_board_value(data_copy)

        if data_copy.turn == 0:

            max_value = -1001
            valid_moves = [c for c in range(7) if data_copy.game_board.is_valid_location(c)]
            # Looking for center moves first in order to find the best move faster:
            center_moves = valid_moves[len(valid_moves) // 3:]
            other_moves = valid_moves[:len(valid_moves) // 3]

            for col in center_moves:

                move_value = MinimaxAgent._alpha_beta(data_copy, col, depth - 1, alpha, beta)
                max_value = max(max_value, move_value)
                alpha = max(alpha, move_value)
                if beta <= alpha:
                    return max_value

            for col in other_moves:

                move_value = MinimaxAgent._alpha_beta(data_copy, col, depth - 1, alpha, beta)
                max_value = max(max_value, move_value)
                alpha = max(alpha, move_value)
                if beta <= alpha:
                    return max_value

            return max_value

        else:

            min_value = 1001
            valid_moves = [col for col in range(7) if data_copy.game_board.is_valid_location(col)]
            # Look for center moves first:
            center_moves = valid_moves[len(valid_moves) // 3:]
            other_moves = valid_moves[:len(valid_moves) // 3]
            for col in center_moves:
                move_value = MinimaxAgent._alpha_beta(data_copy, col, depth - 1, alpha, beta)
                min_value = min(min_value, move_value)
                beta = min(beta, move_value)
                if beta <= alpha:
                    return min_value

            for col in other_moves:
                move_value = MinimaxAgent._alpha_beta(data_copy, col, depth - 1, alpha, beta)
                min_value = min(min_value, move_value)
                alpha = min(alpha, move_value)
                if beta <= alpha:
                    return min_value

            return min_value

    def get_move(self, game_data: GameData) -> int:
        """
        This is the method that have to be called in order to get the move of our MiniMax agent.
        :param game_data: All of the data for the game.
        :return: The chosen col.
        """

        if game_data.game_board.slots_filled == 0:
            return 3
        possible_moves = [col for col in range(7) if game_data.game_board.is_valid_location(col)]
        move_values = [MinimaxAgent._alpha_beta(game_data, move, self.__depth) for move in possible_moves]

        if game_data.turn == 0:
            best_moves = [i for i in possible_moves if move_values[possible_moves.index(i)] == max(move_values)]
        else:
            best_moves = [i for i in possible_moves if move_values[possible_moves.index(i)] == min(move_values)]

        return choice(best_moves)
