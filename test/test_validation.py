import unittest
import sys
sys.path.append('pychess')

import validation
import settings

class FEN_ValidationTest(unittest.TestCase):
    def test_start_position(self):
        self.assertTrue(
            validation.Validation.is_fen(settings.START_POS_FEN))

    def test_seven_rows(self):
        self.assertFalse(
            validation.Validation.is_fen(
                'rnbqkbnr/pp1ppppp/8/2p5/4P3/PPPP1PPP/RNBQKBNR \
                    w KQkq c6 0 2'))

    def test_two_black_kings(self):
        self.assertFalse(validation.Validation.is_code(
            'rnbqkbnr/pppkpppp/8/8/8/8/PPPPPPPP/RNBQKBNR'))

    def test_nine_white_pawns(self):
        self.assertFalse(validation.Validation.is_code(
            'rnbqkbnr/pp1ppppp/8/2p5/4PP2/8/PPPP1PPP/RNBQKBNR'))

    def test_without_black_king(self):
        self.assertFalse(validation.Validation.is_code(
            '8/8/8/8/8/8/8/KQ6'))

    def test_empty_board(self):
        self.assertFalse(validation.Validation.is_code(
            '8/8/8/8/8/8/8/8'))

    @unittest.skip('not implemented')
    def test_three_promotions_and_six_pawns(self):
        self.assertFalse(validation.Validation.is_code(
            'QQRRR3/8/8/8/8/PPPPPPQK/8/k7'))


if __name__ == '__main__':
    unittest.main()
