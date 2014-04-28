import unittest
import sys
sys.path.append('core')

import game

class LegalMovesTest(unittest.TestCase):
    def setUp(self):
        self.game = game.Game(
            '8/8/8/3Kq3/5k2/8/8/8 w - - 0 1')
        self.white_king = self.game.first_piece(['K'], 0)

    def test_queen_attacks(self):
        self.assertIn('d6', self.game.piece_on(
            'e5').attacks)

    def test_white_king_moves(self):
        self.assertEqual({'c6', 'c4'},
            self.white_king.moves)

    def test_cover_check(self):
        self.game.parse_fen('K7/2k5/r7/8/8/8/8/6B1 w - - 0 1')
        bishop = self.game.piece_on('g1')
        king = self.game.piece_on('a8')
        self.assertSetEqual({'a7'}, bishop.moves)

    def test_protection(self):
        black_queen = self.game.piece_on('e5')
        self.assertTrue(self.game.is_protected(black_queen))

    def test_attack_king(self):
        self.assertTrue(self.game.is_under_attack(
            self.white_king))

    def test_king_next_to_each_other(self):
        self.game.parse_fen('8/8/8/3Kk3/5q2/8/8/8 w - - 0 1')
        self.assertFalse(self.game.are_kings_legally_placed())

    def test_enemy_king_under_attack(self):
        self.game._switch_side()
        self.assertFalse(self.game.are_kings_legally_placed())


if __name__ == '__main__':
    unittest.main()
