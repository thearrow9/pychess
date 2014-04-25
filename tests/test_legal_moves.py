import unittest
import sys
sys.path.append('core')

import game

class LegalMovesTest(unittest.TestCase):
    def setUp(self):
        self.game = game.Game()
        self.game.parse_fen('8/8/8/3Kq3/5k2/8/8/8 w - - 0 1')
        self.game.set_moves()
        self.white_king = self.game.first_piece(['K'], 0)

    def test_queen_attacks(self):
        self.assertIn('d6', self.game.piece_on(
            'e5').attacks)

    def test_all_pieces(self):
        self.assertEqual({'d5', 'e5', 'f4'},
            set(piece.location for piece in self.game.pieces_in_play()))

    @unittest.skip('not yet')
    def test_white_king_moves(self):
        self.assertEqual({'c6', 'c4'},
            self.white_king.moves)

    @unittest.skip('not yet')
    def test_legal_moves(self):
        self.assertSetEqual({'c6', 'c4'},
            self.game.legal_moves(
            self.white_king, self.white_king))

    def test_make_illegal_move(self):
        self.game._moved(self.white_king, 'd6')


    def test_attack_king(self):
        self.assertTrue(self.game.is_under_attack(
            self.white_king))

    @unittest.skip('yep')
    def test_king_next_to_each_other(self):
        self.game.parse_fen('8/8/8/3Kk3/5q2/8/8/8 w - - 0 1')
        self.game.record_moves()
        self.assertFalse(self.game.are_kings_legally_placed())

    @unittest.skip('yep')
    def test_enemy_king_under_attack(self):
        self.game._switch_side()
        self.assertFalse(self.game.are_kings_legally_placed())


if __name__ == '__main__':
    unittest.main()
