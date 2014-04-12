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

    def test_top_left_moves(self):
        self.assertEqual({'e3', 'd4', 'c5', 'b6', 'a7'},
            self.game.top_left('f2'))


if __name__ == '__main__':
    unittest.main()
