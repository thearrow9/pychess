import unittest
import sys
sys.path.append('core')

import piece
board  = piece.Board()

class BoardTest(unittest.TestCase):
    def setUp(self):
        self.y = 64

    def test_init(self):
        self.assertEqual(self.y, len(board.squares))

    def test_square_colors(self):
        self.assertEqual(0, board.squares[8].color)

    def test_square_name(self):
        self.assertEqual('b1', str(board.squares[1]))

    def test_square_occupation(self):
        self.assertFalse(board.squares[3].is_occupied())

if __name__ == '__main__':
    unittest.main()
