import unittest
import sys
sys.path.append('../')
from game_board import GameBoard

class TestGameBoard(unittest.TestCase):
	def setUp(self):
		self.board1 = GameBoard()
		self.board2 = GameBoard(5,8)

	def test_init(self):
		self.assertEqual(self.board1.rows,6)
		self.assertEqual(self.board1.cols,7)
		self.assertEqual(self.board1.board[0][0],0)
		self.assertEqual(self.board2.rows,5)
		self.assertEqual(self.board2.cols,8)
		self.assertEqual(self.board2.board[3][6],0)

	def test_drop_piece(self):
		self.board1.drop_piece(1,2,1)
		self.assertEqual(self.board1.board[1][2],1)
		self.board1.drop_piece(0,0,-12)
		self.assertEqual(self.board1.board[0][0],-12)
		self.board1.drop_piece(1,2,4)
		self.assertEqual(self.board1.board[1][2],4)

	def test_get_next_open_row(self):
		self.board1.drop_piece(1,2,1)
		self.board1.drop_piece(0,2,3)
		self.assertEqual(self.board1.board[1][2],1)
		self.assertEqual(self.board1.get_next_open_row(2),2)
		self.assertEqual(self.board1.get_next_open_row(3),0)

	def test_check_square(self):
		self.board1.drop_piece(1,2,1)
		self.board2.drop_piece(4,7,3)
		self.assertEqual(self.board1.check_square(1,1,2),True)
		self.assertEqual(self.board1.check_square(0,1,2),False)
		self.assertEqual(self.board2.check_square(3,4,7),True)
		self.assertEqual(self.board2.check_square(5,8,28),False)
		self.assertEqual(self.board1.check_square(1,100,2),False)
		self.assertEqual(self.board1.check_square(1,-1,2),False)
		self.assertEqual(self.board1.check_square(1,1,2),True)
		self.assertEqual(self.board1.check_square(1,6,2),False)
		self.assertEqual(self.board1.check_square(1,1,7),False)

	def test_horizontal_win(self):
		self.board1.drop_piece(0,0,1)
		self.board1.drop_piece(0,1,1)
		self.board1.drop_piece(0,2,1)
		self.board1.drop_piece(0,3,1)
		self.board1.drop_piece(0,4,1)
		self.assertEqual(self.board1.horizontal_win(1,0,0),True)
		self.assertEqual(self.board1.horizontal_win(2,0,0),False)
		self.assertEqual(self.board1.horizontal_win(8,0,0),False)
		self.assertEqual(self.board1.horizontal_win(1,-156,0),False)

		self.board2.drop_piece(2,1,-67)
		self.board2.drop_piece(2,3,-67)
		self.board2.drop_piece(2,4,-67)
		self.assertEqual(self.board2.horizontal_win(-67,2,1),False)
		self.board2.drop_piece(2,2,-67)
		self.assertEqual(self.board2.horizontal_win(-67,2,1),True)

	def test_vertical_win(self):
		self.board1.drop_piece(1,2,3)
		self.board1.drop_piece(2,2,3)
		self.board1.drop_piece(3,2,3)
		self.assertEqual(self.board1.vertical_win(3,1,2),False)
		self.board1.drop_piece(4,2,4)
		self.assertEqual(self.board1.vertical_win(3,1,2),False)
		self.board1.drop_piece(4,2,3)
		self.assertEqual(self.board1.vertical_win(3,1,2),True)

		self.board2.drop_piece(4,4,-76)
		self.board2.drop_piece(3,4,-76)
		self.board2.drop_piece(2,4,-76)
		self.board2.drop_piece(1,4,-76)
		self.board2.drop_piece(0,4,-76)
		self.assertEqual(self.board2.vertical_win(-76,4,4),False)
		self.assertEqual(self.board2.vertical_win(-76,1,4),True)
		self.assertEqual(self.board2.vertical_win(-76,0,4),True)

	def test_diagonal_win(self):
		self.board1.drop_piece(1,2,3)
		self.board1.drop_piece(2,2,3)
		self.board1.drop_piece(3,2,3)
		self.assertEqual(self.board1.diagonal_win(3,1,2),False)
		self.board1.drop_piece(4,2,4)
		self.assertEqual(self.board1.diagonal_win(3,1,2),False)
		self.board1.drop_piece(2,3,3)
		self.board1.drop_piece(3,4,3)
		self.assertEqual(self.board1.diagonal_win(3,1,2),False)
		self.board1.drop_piece(4,5,3)
		self.assertEqual(self.board1.diagonal_win(3,1,2),True)

		self.assertEqual(self.board2.diagonal_win(0,3,4),True)
		self.board2.drop_piece(4,4,-76)
		self.board2.drop_piece(3,4,0)
		self.board2.drop_piece(2,4,-76)
		self.board2.drop_piece(1,4,-76)
		self.board2.drop_piece(0,4,-76)
		self.assertEqual(self.board2.diagonal_win(0,5,5),False)
		self.board2.drop_piece(4,4,0)
		self.assertEqual(self.board2.diagonal_win(0,5,5),False)
		self.board2.drop_piece(2,5,0)
		self.assertEqual(self.board2.diagonal_win(0,3,4),True)
		self.board2.drop_piece(1,6,-2)
		self.assertEqual(self.board2.diagonal_win(0,3,4),False)

	def test_winning_move(self):
		self.board1.drop_piece(1,2,3)
		self.board1.drop_piece(2,2,3)
		self.board1.drop_piece(3,2,3)
		self.assertEqual(self.board1.winning_move(3),False)
		self.board1.drop_piece(4,2,4)
		self.assertEqual(self.board1.winning_move(3),False)
		self.board1.drop_piece(4,2,3)
		self.assertEqual(self.board1.winning_move(3),True)

		self.assertEqual(self.board2.winning_move(0),True)
		self.board2.drop_piece(4,4,-76)
		self.board2.drop_piece(3,4,0)
		self.board2.drop_piece(2,4,-76)
		self.board2.drop_piece(1,4,-76)
		self.board2.drop_piece(0,4,-76)
		self.assertEqual(self.board2.winning_move(-76),False)
		self.board2.drop_piece(3,4,-76)
		self.assertEqual(self.board2.winning_move(-76),True)
		
	def test_tie_move(self):
		self.board1.drop_piece(1,2,4)
		self.assertEqual(self.board1.tie_move(),False)
		for c in range(self.board1.cols):
			for r in range(self.board1.rows):
				self.board1.drop_piece(r,c,7)
		self.assertEqual(self.board1.tie_move(),True)

		self.assertEqual(self.board2.tie_move(),False)
		for c in range(self.board2.cols):
			for r in range(self.board2.rows):
				self.board2.drop_piece(r,c,-475)
		#self.assertEqual(self.board2.tie_move(),True)
		self.board2.drop_piece(0,3,0)
		self.assertEqual(self.board2.tie_move(),False)

if __name__ == '__main__':
	unittest.main()
  
