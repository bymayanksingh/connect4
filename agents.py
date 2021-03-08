from random import choice
from game_data import GameData
import abc


class Agent(abc.ABC):
	"""
	It is an abstract class. All the agents should inheritance from this class.
	"""

	@staticmethod
	def get_move(game_data: GameData) -> int:
		pass


class RandomAgent(Agent):
	"""
	An agent which makes random moves
	"""

	@staticmethod
	def get_move(data) -> int:
		""" returns a random valid col"""
		return choice([c for c in range(7) if data.game_board.is_valid_location(c)])
