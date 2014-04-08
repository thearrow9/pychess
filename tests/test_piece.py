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


class NotationIter(unittest.TestCase):
    def test_left_iter(self):
        self.assertEqual(['d', 'c', 'b', 'a'],
            [cols for cols in piece.NotationIter.left('e4')])

    def test_up_iter(self):
        self.assertEqual(list(range(2, 9)),
            [rows for rows in piece.NotationIter.up('c1')])

    def test_down_iter(self):
        self.assertEqual(list(range(6, 0, -1)),
            [rows for rows in piece.NotationIter.down('c7')])

    def test_right_iter(self):
        self.assertEqual(['f', 'g', 'h'],
            [cols for cols in piece.NotationIter.right('e6')])

    def test_empty_iter(self):
        self.assertEqual([],
            [cols for cols in piece.NotationIter.right('h2')])

class GameTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.white_king = game.board['e1'].piece

    def test_white_king_location(self):
        self.assertEqual(
            'e1', game.first_piece(['K'], 0).piece.location)

    def test_white_king_instance(self):
        self.assertIsInstance(self.white_king, king)

    def test_white_king_color(self):
        self.assertEqual(self.white_king.color, 0)

    def test_count_pieces_by(self):
        self.assertEqual(1, len(game.pieces_by(['Q'], 1)))

    def test_pieces_in_play(self):
        self.assertEqual(32, len(game.pieces_in_play()))

    def test_get_first(self):
        self.assertIsInstance(game.first_piece(['K'], 1).piece, king)

    def test_to_move(self):
        self.assertEqual(0, game.to_move)

class ValidationTest(unittest.TestCase):
    def test_valid_fen(self):
        self.assertTrue(
            piece.Validation.is_fen(piece.settings.START_POS_FEN))

    def test_invalid_fen(self):
        self.assertFalse(
            piece.Validation.is_fen(
                'rnbqkbnr/pp1ppppp/8/2p5/4P3/PPPP1PPP/RNBQKBNR \
                    w KQkq c6 0 2'))

    def test_three_kings_fen(self):
        self.assertFalse(piece.Validation.correct_pieces(
            'rnbqkbnr/pppkpppp/8/8/8/8/PPPPPPPP/RNBQKBNR'))

    def test_nine_white_pawns_fen(self):
        self.assertFalse(piece.Validation.correct_pieces(
            'rnbqkbnr/pp1ppppp/8/2p5/4PP2/PPPP1PPP/RNBQKBNR'))

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
