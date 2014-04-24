import unittest
import sys
sys.path.append('core')

import board

class BoardTest(unittest.TestCase):
    def setUp(self):
        self.board = board.Board()

    def test_init(self):
        self.assertEqual(64, len(self.board.squares))

    def test_square_colors(self):
        self.assertEqual(0, self.board['d1'].color)
        self.assertEqual(1, self.board['g7'].color)

    def test_square_indexing(self):
        self.assertIs(self.board['c1'], self.board.squares[2])

    def test_square_name(self):
        self.assertEqual('b1', str(self.board.squares[1]))

    def test_square_occupation(self):
        self.assertFalse(self.board['a4'].is_occupied())

    def test_empty_square_type(self):
        self.assertIsNone(self.board['e5'].piece)


if __name__ == '__main__':
    unittest.main()
