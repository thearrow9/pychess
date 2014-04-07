import unittest
import sys
sys.path.append('core')

import piece

board = piece.Board()
game = piece.Game()

class KingTest(unittest.TestCase):
    def setUp(self):
        self.king = piece.CHESS_SET['King']

    def test_points(self):
        self.assertEqual(1000, self.king.points)

class GameTest(unittest.TestCase):
    def setUp(self):
        self.white_king = game.board[4].piece

    def test_king_location(self):
        self.assertIsInstance(self.white_king,
            piece.CHESS_SET['King'])

    #def test_king_color(self):
    #   self.assertEqual(self.white_king.color, 0)

class BoardTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_init(self):
        self.assertEqual(64, len(board.squares))

    def test_opp_square(self):
        self.assertEqual('c2', board.opp_square('c7'))

    @unittest.skip('not implemented')
    def test_square_colors(self):
        pass#self.assertEqual(0, board.squares[8].color)

    def test_square_indexing(self):
        self.assertIs(board[2], board.squares[2])

    def test_square_name(self):
        self.assertEqual('b1', str(board.squares[1]))

    def test_square_occupation(self):
        self.assertFalse(board.squares[3].is_occupied())

    def test_notation_to_id(self):
        self.assertEqual(board.notation_to_id('e1'), 4)

if __name__ == '__main__':
    unittest.main()
