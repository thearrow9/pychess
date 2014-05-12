import unittest
import sys
sys.path.append('core')

import game

class PieceMoveTest(unittest.TestCase):
    def setUp(self):
        self.game = game.Game()
        #build Kg5, Qh6, Re2, Bg6, Nh5, Pf5, Pf4, Pd3, Pb3, Pg2, Ph2
        #kd5, ba4, pa2, pb7, ph4, pe5
        self.game.parse_fen(
            '8/1p6/6BQ/3kpPKN/b4P1p/1P1P4/p3R1PP/8 w - e6 5 55')
        self.rook_e2 = self.game.piece_on('e2')
        self.bishop_g6 = self.game.piece_on('g6')
        self.queen_h6 = self.game.piece_on('h6')
        self.king_g5 = self.game.piece_on('g5')
        self.king_d5 = self.game.piece_on('d5')
        self.knight_h5 = self.game.piece_on('h5')
        self.pawn_g2 = self.game.piece_on('g2')
        self.pawn_h2 = self.game.piece_on('h2')
        self.pawn_a2 = self.game.piece_on('a2')
        self.pawn_b7 = self.game.piece_on('b7')
        self.pawn_b3 = self.game.piece_on('b3')
        self.pawn_f5 = self.game.piece_on('f5')

    #test valid moves

    def test_kg5_moves(self):
        self.assertSetEqual({'f6', 'g4', 'h4'}, self.king_g5.moves)

    def test_pb7_moves(self):
        self.game.switch_side()
        self.game.setup()
        self.assertSetEqual({'b6', 'b5'}, self.pawn_b7.moves)

    def test_pg2_moves(self):
        self.assertSetEqual({'g3', 'g4'}, self.pawn_g2.moves)

    def test_nh5_moves(self):
        self.assertSetEqual({'g3', 'f6', 'g7'}, self.knight_h5.moves)

    def test_re2_moves(self):
        self.assertSetEqual({'a2', 'b2', 'c2', 'd2', 'f2',
            'e1', 'e3', 'e4', 'e5'}, self.rook_e2.moves)

    def test_en_passant_square(self):
        self.assertEqual('e6', self.game.en_passant)

    #test attacks

    def test_pa2_is_attacked(self):
        self.assertTrue(
            self.game.is_under_attack(self.pawn_a2))

    def test_attacked_squares(self):
        self.assertTrue(self.game.is_attacked('b1', 1))

    def test_not_attacked_squares(self):
        self.assertFalse(self.game.is_attacked('a1', 1))

    def test_protect_alias(self):
        self.assertTrue(self.game.is_protected(self.knight_h5))

    def test_black_king_attack(self):
        self.assertSetEqual({'c4', 'e4', 'd4', 'c5', 'e5',
            'c6', 'd6', 'e6'}, self.king_d5.attacks)

    def test_black_attacks(self):
        self.assertSetEqual({'b1', 'b3', 'b5', 'c6', 'd7', 'e8', 'c5',
            'a6', 'g3', 'd4', 'f4', 'd6', 'e6', 'e4', 'c4', 'e5'},
            self.game.all_attacks(1))

    #test legal moves only
    #TODO repair those tests below

    def test_en_passant_move(self):
        self.assertSetEqual({'f6', 'e6'},
            self.pawn_f5.moves)

    def test_rook_e2_moves(self):
        self.assertSetEqual({'a2', 'b2', 'c2', 'd2', 'f2',
            'e1', 'e3', 'e4', 'e5'},
            self.rook_e2.moves)

    def test_pawn_g2_moves(self):
        self.assertSetEqual({'g3', 'g4'},
            self.pawn_g2.moves)

    def test_pawn_h2_moves(self):
        self.assertSetEqual({'h3'},
            self.pawn_h2.moves)

    def test_pawn_b3_moves(self):
        self.assertSetEqual({'b4', 'a4'},
            self.pawn_b3.moves)

    def test_bishop_g6_moves(self):
        self.assertSetEqual({'h7', 'f7', 'e8'},
            self.bishop_g6.moves)

    def test_queen_h6_moves(self):
        self.assertSetEqual({'h7', 'g7', 'f8', 'h8'},
            self.queen_h6.moves)

    def test_king_g5_moves(self):
        self.assertSetEqual({'f6', 'g4', 'h4'},
            self.king_g5.moves)

    def test_knight_h5_moves(self):
        self.assertSetEqual({'g3', 'g7', 'f6'},
            self.knight_h5.moves)


if __name__ == '__main__':
    unittest.main()
