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
        self.black = self.game.pieces_by_color(1)

    def test_white_king_location(self):
        self.assertEqual(
            'e1', self.game.first_piece(['K'], 0).location)

    def test_white_king_instance(self):
        self.assertIsInstance(self.white_king, self.king)

    def test_white_king_color(self):
        self.assertEqual(self.white_king.color, 0)

    def test_pieces_by_color(self):
        self.assertEqual('a7', self.black[0].location)

    def test_len_pieces_by_color(self):
        self.assertEqual(16, len(self.black))

    def test_count_pieces_by(self):
        self.assertEqual(1, len(self.game.pieces_by(['Q'], 1)))

    def test_pieces_in_play(self):
        self.assertEqual(32, len(self.game.pieces_in_play()))

    def test_get_first(self):
        self.assertIsInstance(self.game.first_piece(['K'], 1), self.king)

    def test_to_move(self):
        self.assertEqual(0, self.game.to_move)


if __name__ == '__main__':
    unittest.main()
