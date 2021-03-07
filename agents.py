from random import choice
from game_data import GameData
import abc


class Agent(abc.ABC):

	@staticmethod
	def get_move(game_data: GameData) -> int:
		pass


class RandomAgent(Agent):

	@staticmethod
	def get_move(data) -> int:
		""" returns a random valid col"""
		return choice([c for c in range(7) if data.game_board.is_valid_location(c)])
