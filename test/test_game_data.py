import unittest
import sys
sys.path.append('../')
from game_data import GameData 

class TestGameData(unittest.TestCase):
	def setUp(self):
		self.data1 = GameData()

	def test_init(self):
		self.assertFalse(self.data1.game_over)
		self.assertEqual(self.data1.turn,0)
		self.assertEqual(self.data1.last_move_row,[])
		self.assertEqual(self.data1.last_move_col,[])
		self.assertEqual(self.data1.action,None)
		self.assertEqual(self.data1.game_board.rows,6)
		self.assertEqual(self.data1.game_board.cols,7)



if __name__ == '__main__':
	unittest.main()