import unittest
import sys
sys.path.append('core')

import settings
import piece
from notation import Notation

class NotationTest(unittest.TestCase):
    def test_str_to_coords(self):
        self.assertEqual([2, 4], Notation.str_to_coords('e3'))

    def test_coords_to_str(self):
        self.assertEqual('h5', Notation.coords_to_str([4, 7]))

    def test_all_squares(self):
        self.assertEqual('a8',
            Notation.all_squares(True)[0])
        self.assertEqual('a1',
            Notation.all_squares()[0])

    def test_opp_square(self):
        self.assertEqual('c2', Notation.opp_square('c7'))

    def test_squares_between(self):
        self.assertSetEqual({'a7', 'a8'}, Notation.squares_between('a7', 'a8'))
        self.assertSetEqual({'a2', 'a3', 'a4', 'a5'}, Notation.squares_between('a2', 'a5'))
        self.assertSetEqual({'a2', 'b3', 'c4', 'd5'}, Notation.squares_between('a2', 'd5'))
        self.assertSetEqual({'e5', 'd5'}, Notation.squares_between('e5', 'd5'))
        self.assertSetEqual({'h1', 'g2', 'f3', 'e4'},
            Notation.squares_between('e4', 'h1'))


if __name__ == '__main__':
    unittest.main()
