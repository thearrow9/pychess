import unittest
import sys
sys.path.append('core')

import game

class PlacePieceTest(unittest.TestCase):
    def setUp(self):
        self.game = game.Game('8/8/8/3Kq3/2p2k2/8/pP6/8 w - - 0 1')
        self.wk = self.game.piece_on('d5')
        self.bk = self.game.piece_on('f4')
        self.pa2 = self.game.piece_on('a2')
        self.pb2 = self.game.piece_on('b2')
        self.pc4 = self.game.piece_on('c4')

    def test_create_fen_after_move(self):
        self.game.play(self.wk, 'c4')
        self.assertEqual(
            '8/8/8/4q3/2K2k2/8/pP6/8', self.game._encode_pieces())

    def test_simple_move(self):
        self.game.play(self.wk, 'c4')
        self.assertEqual('c4', self.wk.location)
        self.assertFalse(self.game.board['d5'].is_occupied())

    def test_move_white_king(self):
        self.game.play(self.wk, 'c4')
        piece_locations = set(
            piece.location for piece in self.game.pieces_in_play())
        self.assertTrue('c4' in piece_locations and \
            'd5' not in piece_locations)

    def test_move_white_king_and_undo(self):
        self.game.play(self.wk, 'c6')
        self.game._undo_last_move()
        self.assertEqual(
            '8/8/8/3Kq3/2p2k2/8/pP6/8', self.game._encode_pieces())

    def test_capture_and_undo_it(self):
        self.game.play(self.wk, 'c4')
        self.assertTrue(self.game._undo_last_move())
        self.assertEqual(
            '8/8/8/3Kq3/2p2k2/8/pP6/8', self.game._encode_pieces())

    def test_illegal_move(self):
        self.game.play(self.wk, 'd6')
        self.assertFalse(self.game.is_valid_position())

    def test_en_passant_move(self):
        self.game.parse_fen('8/8/8/8/p6k/K7/1P6/8 w - - 0 1')
        self.game.play_('b2', 'b4')
        self.game.play_('a4', 'b3')
        self.assertEqual('8/8/8/8/7k/Kp6/8/8', self.game._encode_pieces())

    def test_promotion(self):
        self.game.play(self.wk, 'c4')
        self.game.play(self.pa2, 'a1=Q')
        self.assertEqual('q', self.game.piece_on('a1').code)

    def test_castle(self):
        self.game.parse_fen('8/8/k7/8/8/8/8/R3K2R w KQ - 10 20')
        white_king = self.game.piece_on('e1')
        self.assertSetEqual({'d1', 'd2', 'e2', 'f2', 'f1', 'g1', 'c1'},
            white_king.moves)


if __name__ == '__main__':
    unittest.main()
