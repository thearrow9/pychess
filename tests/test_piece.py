import unittest
import sys
sys.path.append('core')

import settings
import piece

class PieceTest(unittest.TestCase):
    def setUp(self):
        self.king = settings.CHESS_SET['K']
        self.queen = settings.CHESS_SET['Q']

    def test_king_points(self):
        self.assertEqual(1000, self.king.points)

    def test_king_long_move(self):
        self.assertFalse(self.king.long_move)

    def test_king_label(self):
        self.assertEqual('King', self.king.label)

    def test_queen_points(self):
        self.assertEqual(9, self.queen.points)

    def test_queen_label(self):
        self.assertEqual('Queen', self.queen.label)


if __name__ == '__main__':
    unittest.main()
