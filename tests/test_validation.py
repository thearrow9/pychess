import unittest
import sys
sys.path.append('core')

import validation
import settings

class ValidationTest(unittest.TestCase):
    def test_valid_fen(self):
        self.assertTrue(
            validation.Validation.is_fen(settings.START_POS_FEN))

    def test_invalid_fen(self):
        self.assertFalse(
            validation.Validation.is_fen(
                'rnbqkbnr/pp1ppppp/8/2p5/4P3/PPPP1PPP/RNBQKBNR \
                    w KQkq c6 0 2'))

    def test_three_kings_fen(self):
        self.assertFalse(validation.Validation.is_legal(
            'rnbqkbnr/pppkpppp/8/8/8/8/PPPPPPPP/RNBQKBNR'))

    def test_nine_white_pawns_fen(self):
        self.assertFalse(validation.Validation.is_legal(
            'rnbqkbnr/pp1ppppp/8/2p5/4PP2/PPPP1PPP/RNBQKBNR'))


if __name__ == '__main__':
    unittest.main()
