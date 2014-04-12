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
        #build Kg5, Qh6, Re2, Bg6, Nh5, Pf4, Pd3, Pb3, Ph2, kd5, pa2
        self.game.parse_fen('8/8/6BQ/3k2KN/5P2/1P1P4/p3R2P/8 w - 5 55')
        self.rook_e2 = self.game.piece_on('e2')
        self.bishop_g6 = self.game.piece_on('g6')
        self.queen_h6 = self.game.piece_on('h6')
        self.king_g5 = self.game.piece_on('g5')

    def test_rook_e2_moves(self):
        self.assertEqual({'a2', 'b2', 'c2', 'd2', 'f2', 'g2', \
            'e1', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8'},
            self.game.possible_moves(self.rook_e2))

    def test_bishop_g6_moves(self):
        self.assertEqual({'h7', 'f7', 'e8', 'f5', 'e4'}, \
            self.game.possible_moves(self.bishop_g6))

    def test_queen_h6_moves(self):
        self.assertEqual({'h7', 'g7', 'f8', 'h8'}, \
            self.game.possible_moves(self.queen_h6))

    def test_king_g5_moves(self):
        self.assertEqual({'f6', 'f5', 'g4', 'h4'}, \
            self.game.possible_moves(self.king_g5))


    def test_piece_on_way(self):
        self.assertEqual(
            self.game.piece_on_way(self.rook_e2, 'h2'), [[]])


class MoveRuleTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game = game.Game()
        #build Kh2, Rh1, kf2, ra1
        self.game.parse_fen('8/8/8/8/8/8/5k1K/r6R w - 5 55')

    def test_pieces_in_play(self):
        self.assertEqual(4, len(self.game.pieces_in_play()))

    def test_left_moves(self):
        self.assertEqual({'g1', 'f1', 'e1', 'd1', 'c1', 'b1', 'a1'},
            self.game.left('h1'))

    def test_up_moves(self):
        self.assertEqual({'f3', 'f4', 'f5', 'f6', 'f7', 'f8'},
            self.game.up('f2'))

    def test_down_moves(self):
        self.assertEqual({'f1'}, self.game.down('f2'))

    def test_right_moves(self):
        self.assertEqual({'g2', 'h2'}, self.game.right('f2'))

    def test_empty_moves(self):
        self.assertEqual(set(), self.game.down('a1'))

    def test_alias_on_way(self):
        self.assertEqual(set(), self.game.down('h2'))

    def test_up_left_moves(self):
        self.assertEqual({'e3', 'd4', 'c5', 'b6', 'a7'},
            self.game.up_left('f2'))

    def test_up_right_moves(self):
        self.assertEqual({'g3', 'h4'}, self.game.up_right('f2'))

    def test_down_left_moves(self):
        self.assertEqual({'e3', 'd2', 'c1'}, self.game.down_left('f4'))

    def test_down_right_moves(self):
        self.assertEqual({'g4', 'h3'}, self.game.down_right('f5'))


if __name__ == '__main__':
    unittest.main()
