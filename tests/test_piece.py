import unittest
import sys
sys.path.append('core')

import piece

board = piece.Board()
game = piece.Game()
king = piece.CHESS_SET['King']

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
        self.assertEqual('K', king.label)

class GameTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.white_king = game.board['e1'].piece

    def test_white_king_location(self):
        self.assertEqual(
            'e1', game.select_first('K', 0).piece.location)

    def test_white_king_instance(self):
        self.assertIsInstance(self.white_king,
            piece.CHESS_SET['King'])

    def test_white_king_color(self):
       self.assertEqual(self.white_king.color, 0)

    def test_count_select_all(self):
        self.assertEqual(1, len(game.select_all('Q', 1)))

    def test_select_first(self):
        self.assertIsInstance(
            game.select_first('K', 1).piece, piece.CHESS_SET['King'])

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
        self.assertFalse(board.squares[3].is_occupied())

    def test_notation_to_id(self):
        self.assertEqual(board.notation_to_id('e1'), 4)

if __name__ == '__main__':
    unittest.main()
