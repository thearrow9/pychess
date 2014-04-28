import unittest
import sys
sys.path.append('core')

import game
import errors

class ValidPositionTest(unittest.TestCase):
    def setUp(self):
        self.game = game.Game(
            '8/8/8/3Kq3/2p2k2/8/pP6/8 w - - 0 1')
        self.wk = self.game.piece_on('d5')
        self.validate = self.game.is_valid_position

    def test_current_position(self):
        self.assertTrue(self.validate())

    def test_black_to_move(self):
        self.game._switch_side()
        self.assertFalse(self.validate())

    def test_white_plays_illegal_move(self):
        self.game.play(self.wk, 'd4')
        self.assertFalse(self.validate())

    def test_white_takes_protected_piece(self):
        self.game.play(self.wk, 'e5')
        self.assertFalse(self.validate())

    def test_kings_next_to_each_other(self):
        self.game.parse_fen('8/8/8/8/8/8/8/Kkr5 w - - 0 1')
        self.assertFalse(self.validate())
        self.game._switch_side()
        self.assertFalse(self.validate())

    def test_king_is_missing(self):
        with self.assertRaises(errors.InputError):
            self.game.parse_fen('8/8/8/8/8/8/8/KQ6 w - - 0 1')


if __name__ == '__main__':
    unittest.main()
