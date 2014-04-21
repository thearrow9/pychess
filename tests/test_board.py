import unittest
import sys
sys.path.append('core')

import board

class BoardTest(unittest.TestCase):
    def setUp(self):
        self.board = board.Board()

    def test_init(self):
        self.assertEqual(64, len(self.board.squares))

    def test_opp_square(self):
        self.assertEqual('c2', self.board.opp_square('c7'))

    def test_square_colors(self):
        self.assertEqual(0, self.board.squares[8].color)

    def test_square_indexing(self):
        self.assertIs(self.board['c1'], self.board.squares[2])

    def test_square_name(self):
        self.assertEqual('b1', str(self.board.squares[1]))

    def test_square_occupation(self):
        self.assertFalse(self.board['a4'].is_occupied())

    def test_str_to_coords(self):
        self.assertEqual([2, 4], self.board.str_to_coords('e3'))

    def test_coords_to_str(self):
        self.assertEqual('h5', self.board.coords_to_str([4, 7]))

#TODO remove the rest

    def test_str_to_index(self):
        self.assertEqual(self.board.str_to_index('e1'), 4)


if __name__ == '__main__':
    unittest.main()
