import unittest
import sys
sys.path.append('core')

import game

class MovePieceTest(unittest.TestCase):
    def setUp(self):
        self.game = game.Game()
        self.game.parse_fen('8/8/8/3Kq3/2p2k2/8/pP6/8 w - - 0 1')
        self.white_king = self.game.piece_on('d5')
        self.black_king = self.game.piece_on('f4')
        self.pa2 = self.game.piece_on('a2')
        self.pb2 = self.game.piece_on('b2')
        self.pc4 = self.game.piece_on('c4')

    def test_create_fen_after_move(self):
        self.game.make_move(self.white_king, 'c4')
        self.assertEqual('c4', self.white_king.location)
        fen = self.game._create_fen()
        self.assertEqual('8/8/8/4q3/2K2k2/8/pP6/8', fen)

    def test_simple_move(self):
        self.game.board['c4'] = self.white_king
        self.game.board['d5'] = None
        self.assertEqual('c4', self.white_king.location)

    def test_move_white_king_to_c6(self):
        self.game.make_move(self.white_king, 'c4')
        piece_locations = set(piece.location for piece in self.game.pieces_in_play())
        self.assertTrue('c4' in piece_locations and \
            'd5' not in piece_locations)

    def test_move_kd5_to_c6_and_undo(self):
        self.game.make_move(self.white_king, 'c6')
        self.assertTrue(self.game._undo_last_move())
        self.assertEqual('d5', self.game.first_piece(['K'], 0).location)
        self.assertFalse(self.game.board['c6'].is_occupied())

    def test_capture_and_undo_it(self):
        self.game.make_move(self.white_king, 'c4')
        self.game._undo_last_move()
        self.assertTrue(self.game.board['c4'].is_occupied())

    def test_make_illegal_move(self):
        self.game.make_move(self.white_king, 'd6')
        self.assertFalse(self.game.is_valid_position())

    def test_make_en_passant_move(self):
        self.game.make_move(self.white_king, 'c6')
        self.game.make_move(self.black_king, 'f5')
        self.game.make_move(self.pb2, 'b4')
        self.assertEqual({'b3', 'c3'}, self.pc4.moves)

    @unittest.skip('not yet')
    def test_promotion(self):
        self.game.make_move(self.white_king, 'c4')
        self.game.make_move(self.pa2, 'a1')



if __name__ == '__main__':
    unittest.main()
