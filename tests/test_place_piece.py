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
        self.game.play(self.wk.location, 'c4')
        self.assertEqual(
            '8/8/8/4q3/2K2k2/8/pP6/8', self.game._encode_pieces())

    def test_simple_move(self):
        self.game.play(self.wk.location, 'c4')
        self.assertEqual('c4', self.wk.location)
        self.assertFalse(self.game.board['d5'].is_occupied())

    def test_move_white_king(self):
        self.game.play(self.wk.location, 'c4')
        piece_locations = set(
            piece.location for piece in self.game.pieces_in_play())
        self.assertTrue('c4' in piece_locations and \
            'd5' not in piece_locations)

    def test_move_white_king_andundo(self):
        self.game.play(self.wk.location, 'c6')
        self.game.undo_last_move()
        self.assertEqual(
            '8/8/8/3Kq3/2p2k2/8/pP6/8', self.game._encode_pieces())

    def test_capture_andundo_it(self):
        self.game.play(self.wk.location, 'c4')
        self.assertTrue(self.game.undo_last_move())
        self.assertEqual(
            '8/8/8/3Kq3/2p2k2/8/pP6/8', self.game._encode_pieces())

    def test_illegal_move(self):
        self.game.play(self.wk.location, 'd6')
        self.assertFalse(self.game.is_valid_position())

    def test_en_passant_move(self):
        self.game.parse_fen('8/8/8/8/p6k/K7/1P6/8 w - - 0 1')
        self.game.play('b2', 'b4')
        self.game.play('a4', 'b3')
        self.assertEqual('8/8/8/8/7k/Kp6/8/8', self.game._encode_pieces())

    def test_promotion(self):
        self.game.play(self.wk.location, 'c4')
        self.game.play('a2', 'a1=Q')
        self.assertEqual('q', self.game.piece_on('a1').code)

    def test_castle_move(self):
        self.game.parse_fen('8/8/k7/8/8/8/8/R3K2R w KQ - 10 20')
        self.game.play('e1', 'g1')
        self.assertEqual('8/8/k7/8/8/8/8/R4RK1',
            self.game._encode_pieces())

    def test_king_move_disable_castle(self):
        self.game.parse_fen('8/8/k7/8/8/8/8/R3K2R w KQ - 10 20')
        self.game.play('e1', 'e2')
        self.assertTrue(self.game.save_position().startswith(
            '8/8/k7/8/8/8/4K3/R6R b - '))

    def test_rook_move_disable_castle(self):
        self.game.parse_fen('8/8/k7/8/8/8/8/R3K2R w KQ - 10 20')
        self.game.play('a1', 'a3')
        self.assertTrue(self.game.save_position().startswith(
            '8/8/k7/8/8/R7/8/4K2R b K '))

    def test_play_opening(self):
        self.game = game.Game()
        self.game.play('e2', 'e4')
        self.assertEqual('rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1',
            self.game.save_position())
        self.game.play('c7', 'c5')
        self.assertEqual('rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq c6 0 2',
            self.game.save_position())
        self.game.play('g1', 'f3')
        self.assertEqual('rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2',
            self.game.save_position())

    def test_play_and_undo_twice(self):
        self.game = game.Game()
        self.game.play('e2', 'e4')
        self.game.play('c7', 'c5')
        self.game.play('g1', 'f3')
        self.game.undo_last_move()
        self.game.undo_last_move()
        self.assertEqual('rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1',
            self.game.save_position())


if __name__ == '__main__':
    unittest.main()
