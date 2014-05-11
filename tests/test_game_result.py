import unittest
import sys
sys.path.append('core')

import game

class GameResultTest(unittest.TestCase):
    def setUp(self):
        self.game = game.Game('8/8/8/8/8/8/5Q2/5K1k b - - 10 20')

    def test_stalemate(self):
        self.assertTrue(self.game.is_stalemate())

    def test_checkmate(self):
        self.game.parse_fen('8/8/8/8/8/8/5Q2/5K1k w - - 10 20')
        self.game.play_('f2', 'g2')
        self.assertTrue(self.game.is_checkmate())

    def test_50_move_rule_draw(self):
        self.game.parse_fen('8/8/8/8/8/8/8/K3kb2 w - - 49 102')
        self.game.play_('a1', 'a2')
        self.assertTrue(self.game.is_fifty_move_draw())

    def test_treefold_repetition_draw(self):
        for x in range(3):
            self.game.play_('f2', 'e1')
            self.game.play_('h1', 'h2')
            self.game.play_('e1', 'f2')
            self.game.play_('h2', 'h1')
        self.assertTrue(self.game.is_treefold_draw())

    def test_two_kings(self):
        self.game.parse_fen('8/8/8/8/8/8/8/K2k4 w - - 12 92')
        self.assertTrue(self.game.is_theoretical_draw())

    def test_theoretical_draw(self):
        self.game.parse_fen('8/8/8/8/8/8/8/KNk5 w - - 12 92')
        self.assertTrue(self.game.is_theoretical_draw())


if __name__ == '__main__':
    unittest.main()
