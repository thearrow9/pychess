import unittest
import sys
sys.path.append('core')

import settings
import piece
import notation

class NotationTest(unittest.TestCase):
    def test_str_to_coords(self):
        self.assertEqual([2, 4], notation.Notation.str_to_coords('e3'))

    def test_coords_to_str(self):
        self.assertEqual('h5', notation.Notation.coords_to_str([4, 7]))


if __name__ == '__main__':
    unittest.main()
