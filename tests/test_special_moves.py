import unittest
import sys
sys.path.append('core')

import game

class CastleTest(unittest.TestCase):
    def setUp(self):
        self.game = game.Game(
            'r3k2r/pp3p1p/7B/2q5/6B1/2NP4/PPPQ4/R3K2R w KQkq - 1 25')

    def test_white_short_castle(self):
        self.assertFalse(self.game.is_legal_short_castle(0))

    def test_white_long_castle(self):
        self.assertTrue(self.game.is_legal_long_castle(0))

    def test_black_short_castle(self):
        self.assertFalse(self.game.is_legal_short_castle(1))

    def test_black_long_castle(self):
        self.assertFalse(self.game.is_legal_long_castle(1))

    def test_remove_bh6_black_short_castle(self):
        self.game.board['h6'].piece = None
        self.assertTrue(self.game.is_legal_short_castle(1))

    def test_remove_bg4_black_long_castle(self):
        self.game.board['g4'].piece = None
        self.assertTrue(self.game.is_legal_long_castle(1))

    def test_ke1_under_attack_by_pf2(self):
        self.game.parse_fen(
            'r3k2r/pp3p1p/7B/2q5/6B1/2NP4/PPPQ1p2/R3K2R w KQkq - 1 25')
        self.assertFalse(self.game.is_legal_short_castle(0))
        self.assertFalse(self.game.is_legal_long_castle(0))


if __name__ == '__main__':
    unittest.main()
