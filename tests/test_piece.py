import unittest
import sys
sys.path.append('core')

import piece

board = piece.Board()
game = piece.Game()
king = piece.CHESS_SET['K']

class KingTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_points(self):
        self.assertEqual(1000, king.points)

    def test_long_move(self):
        self.assertFalse(king.long_move)

    def test_start_pos(self):
        self.assertEqual('e1', king.start_pos[0])

    def test_count_start_pos(self):
        self.assertEqual(1, len(king.start_pos))

    def test_label(self):
        self.assertEqual('King', king.label)

class GameTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.white_king = game.board['e1'].piece

    def test_white_king_location(self):
        self.assertEqual(
            'e1', game.get_first('K', 0).piece.location)

    def test_white_king_instance(self):
        self.assertIsInstance(self.white_king, king)

    def test_white_king_color(self):
        self.assertEqual(self.white_king.color, 0)

    def test_count_get_all_by(self):
        self.assertEqual(1, len(game.get_all_by('Q', 1)))

    def test_piece_in_play(self):
        self.assertEqual(32, len(game.get_all_in_play()))

    def test_get_first(self):
        self.assertIsInstance(game.get_first('K', 1).piece, king)

    def test_valid_fen(self):
        self.assertTrue(
            game.is_valid_fen(piece.settings.START_POS_FEN))

    def test_invalid_fen(self):
        self.assertFalse(
            game.is_valid_fen(
                'rnbqkbnr/pp1ppppp/8/2p5/4P3/PPPP1PPP/RNBQKBNR\
                    w KQkq c6 0 2'))

class BoardTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_init(self):
        self.assertEqual(64, len(board.squares))

    def test_opp_square(self):
        self.assertEqual('c2', board.opp_square('c7'))

    def test_square_colors(self):
        self.assertEqual(0, board.squares[8].color)

    def test_square_indexing(self):
        self.assertIs(board['c1'], board.squares[2])

    def test_square_name(self):
        self.assertEqual('b1', str(board.squares[1]))

    def test_square_occupation(self):
        self.assertFalse(board['a4'].is_occupied())

    def test_str_to_index(self):
        self.assertEqual(board.str_to_index('e1'), 4)

if __name__ == '__main__':
    unittest.main()
