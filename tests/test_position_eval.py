import unittest
import sys
sys.path.append('core')

import game

class PositionEvalTest(unittest.TestCase):
    def setUp(self):
        self.game = game.Game('8/8/8/8/8/8/5Q2/5K1k w - - 10 20')
        self.white = self.game.pieces_by_color(0)
        self.black = self.game.pieces_by_color(1)

    def test_list_all_moves(self):
        self.game.play('f2', 'e1')
        self.game.play('h1', 'h2')
        self.game.play('e1', 'f2')
        self.assertEqual({'h2-h1', 'h2-h3'}, self.game.list_moves())

    def test_eval_material(self):
        self.assertEqual(9, self.game.eval_material(self.white, self.black))

    @unittest.skip('not yet')
    def test_pawn_structure(self):
        pass

    def test_piece_activity(self):
        self.assertEqual(202, self.game.eval_piece_activity(
            self.white, self.black))

    def test_eval_position(self):
        self.assertTrue(50 > self.game.eval_position() > 10)

    def test_eval_king_position(self):
        self.assertEqual(22, self.game.eval_kings_position(
            self.white, self.black))

    def test_eval_start_position(self):
        self.game.parse_fen('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
        white, black = self.game.pieces_by_color(0), self.game.pieces_by_color(1)
        self.assertEqual(0, self.game.eval_position())

    def test_eval_sicilian_defence(self):
        self.game.parse_fen('rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1')
        self.assertTrue(0.5 > self.game.eval_position() > 0)

    def test_eval_checkmate(self):
        self.game.parse_fen('7K/q7/7k/8/8/8/8/8 b - - 10 39')
        self.game.play('a7', 'b8')
        self.assertEqual(-1000, self.game.eval_position())

    def test_eval_stalemate(self):
        self.game.parse_fen('k1K5/1R6/7P/8/8/8/8/8 w - - 30 112')
        self.game.play('c8', 'c7')
        self.assertEqual(0, self.game.eval_position())

    def test_draw_position(self):
        self.game.parse_fen('kNK5/8/8/8/8/8/8/8 w - - 20 100')
        self.assertEqual(0, self.game.eval_position())

    @unittest.skip('not ready')
    def test_evalutate_init_position(self):
        self.assertEqual({}, self.game.evaluate())

    @unittest.skip('not ready')
    def test_mate_in_one(self):
        #self.game.evaluate(max_depth = 2)
        move_marks = self.game.eval_moves(2)
        self.assertSetEqual({'f2g2', 'f2h4'}, self.game.eval_moves())


if __name__ == '__main__':
    unittest.main()
