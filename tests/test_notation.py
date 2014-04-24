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


if __name__ == '__main__':
    unittest.main()
