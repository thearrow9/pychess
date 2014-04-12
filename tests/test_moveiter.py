import unittest
import sys
sys.path.append('core')

import moveiter

class MoveIterTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.obj = moveiter.MoveIter()
        self.iter1 = self.obj.col_iter('d6', 1)
        self.iter2 = self.obj.row_iter('d6', -1)

    def test_col_iter(self):
        self.assertEqual(['c', 'b', 'a'], \
            [x for x in self.obj.col_iter('d4', -1)])

    def test_row_iter(self):
        self.assertEqual(['3', '4', '5', '6', '7', '8'], \
            [x for x in self.obj.row_iter('d2', 1)])

    def test_diagonal_gen(self):
        self.assertEqual(['e5', 'f4', 'g3', 'h2'],
            [x for x in self.obj.diagonal_gen(
                self.iter1, self.iter2)])


if __name__ == '__main__':
    unittest.main()
