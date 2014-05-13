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
        self.game.switch_side()
        self.game.play('f2', 'g2')
        self.assertFalse(self.game.is_draw())
        self.assertTrue(self.game.is_checkmate())

    def test_50_move_rule_draw(self):
        self.game.parse_fen('8/8/8/8/8/8/8/K3kb2 w - - 49 102')
        self.game.play('a1', 'a2')
        self.assertTrue(self.game.is_fifty_move_draw())

    def test_49_half_moves_and_capture(self):
        self.game.parse_fen('8/8/8/8/8/8/8/RbK4k w - - 49 55')
        self.game.play('a1', 'b1')
        self.assertFalse(self.game.is_fifty_move_draw())

    def test_49_half_move_and_pawn_move(self):
        self.game.parse_fen('8/8/8/8/8/8/P6k/K7 w - - 49 30')
        self.game.play('a2', 'a4')
        self.assertFalse(self.game.is_fifty_move_draw())

    def test_promote_bishop_having_3_pieces_on_board(self):
        self.game.parse_fen('8/8/8/8/8/8/p6k/1R5K b - - 20 91')
        self.game.play('a2', 'b1=B')
        self.assertTrue(self.game.is_draw())

    def test_treefold_repetition_draw(self):
        for x in range(3):
            self.game.play('f2', 'e1')
            self.game.play('h1', 'h2')
            self.game.play('e1', 'f2')
            self.game.play('h2', 'h1')
        self.assertTrue(self.game.is_treefold_draw())

    def test_two_kings(self):
        self.game.parse_fen('8/8/8/8/8/8/8/K2k4 w - - 12 92')
        self.assertTrue(self.game.is_impossible_to_checkmate())

    def test_impossible_to_checkmate(self):
        self.game.parse_fen('8/8/8/8/8/8/8/KNk5 w - - 12 92')
        self.assertTrue(self.game.is_impossible_to_checkmate())


if __name__ == '__main__':
    unittest.main()
