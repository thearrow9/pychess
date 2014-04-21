import unittest
import sys
sys.path.append('core')

import game

class GameTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game = game.Game()
        self.white_king = self.game.piece_on('e1')
        self.king = game.settings.CHESS_SET['K']

    def test_white_king_location(self):
        self.assertEqual(
            'e1', self.game.first_piece(['K'], 0).location)

    def test_white_king_instance(self):
        self.assertIsInstance(self.white_king, self.king)

    def test_white_king_color(self):
        self.assertEqual(self.white_king.color, 0)

    def test_count_pieces_by(self):
        self.assertEqual(1, len(self.game.pieces_by(['Q'], 1)))

    def test_pieces_in_play(self):
        self.assertEqual(32, len(self.game.pieces_in_play()))

    def test_get_first(self):
        self.assertIsInstance(self.game.first_piece(['K'], 1), self.king)

    def test_to_move(self):
        self.assertEqual(0, self.game.to_move)


class PieceMoveTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game = game.Game()
        #build Kg5, Qh6, Re2, Bg6, Nh5, Pf4, Pd3, Pb3, Pg2, Ph2
        #kd5, ba4, pa2, pb7, ph4
        self.game.parse_fen('8/1p6/6BQ/3k2KN/b4P1p/1P1P4/p3R1PP/8 w - 5 55')
        self.rook_e2 = self.game.piece_on('e2')
        self.bishop_g6 = self.game.piece_on('g6')
        self.queen_h6 = self.game.piece_on('h6')
        self.king_g5 = self.game.piece_on('g5')
        self.knight_h5 = self.game.piece_on('h5')
        self.pawn_g2 = self.game.piece_on('g2')
        self.pawn_h2 = self.game.piece_on('h2')
        self.pawn_b7 = self.game.piece_on('b7')
        self.pawn_b3 = self.game.piece_on('b3')

    #test all moves

    def test_kg5_moves(self):
        self.assertEqual({'f5', 'f6', 'f4', 'g4', 'g6', 'h4',
            'h5', 'h6'}, self.king_g5.all_moves())

    def test_pb7_moves(self):
        self.assertEqual({'b6', 'b5', 'a6', 'c6'},
            self.pawn_b7.all_moves())

    def test_pg2_moves(self):
        self.assertEqual({'h3', 'f3', 'g3', 'g4'},
            self.pawn_g2.all_moves())

    def test_nh5_moves(self):
        self.assertEqual({'f4', 'g3', 'f6', 'g7'},
            self.knight_h5.all_moves())

    def test_re2_moves(self):
        self.assertEqual({'a2', 'b2', 'c2', 'd2', 'f2', 'g2', 'h2',
            'e1', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8'},
            self.rook_e2.all_moves())

    #test possible moves only

    def test_rook_e2_moves(self):
        self.assertEqual({'a2', 'b2', 'c2', 'd2', 'f2',
            'e1', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8'},
            self.game.possible_moves(self.rook_e2))

    def test_pawn_g2_moves(self):
        self.assertEqual({'g3', 'g4'},
            self.game.possible_moves(self.pawn_g2))

    def test_pawn_h2_moves(self):
        self.assertEqual({'h3'},
            self.game.possible_moves(self.pawn_h2))

    def test_pawn_b3_moves(self):
        self.assertEqual({'b4', 'a4'},
            self.game.possible_moves(self.pawn_b3))

    def test_bishop_g6_moves(self):
        self.assertEqual({'h7', 'f7', 'e8', 'f5', 'e4'},
            self.game.possible_moves(self.bishop_g6))

    def test_queen_h6_moves(self):
        self.assertEqual({'h7', 'g7', 'f8', 'h8'},
            self.game.possible_moves(self.queen_h6))

    def test_king_g5_moves(self):
        self.assertEqual({'f6', 'f5', 'g4', 'h4'},
            self.game.possible_moves(self.king_g5))

    def test_knight_h5_moves(self):
        self.assertEqual({'g3', 'g7', 'f6'},
            self.game.possible_moves(self.knight_h5))


if __name__ == '__main__':
    unittest.main()
