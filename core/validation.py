import re

class Validation:
    @classmethod
    def is_fen(self, fen):
        code, *args = fen.split(' ')
        return bool(re.match(
            '^({0}\/){{7}}{0} [wb] (-|K?Q?k?q?) (-|[a-h][36]) \d+ \d+'. \
                format('[rbnqkpRBNQKP1-8]{1,8}'), fen)) \
                    and self.is_code(code)

    @classmethod
    def is_code(self, code):
        default_count = {'K': 1, 'Q': 1, 'R': 2, 'B': 2, 'N': 2, 'P': 8}

        pieces = ['K', 'Q', 'R', 'B', 'N', 'P', 'k', 'q', 'r', 'b', 'n', 'p']
        counts = dict((x, code.count(x)) for x in pieces)

        promotions = dict((x, counts[x] - default_count[x.upper()]) for x in counts)
        #TODO more validations are required
        return counts['K'] == 1 and counts['k'] == 1 and \
            counts['P'] <= 8 and counts['p'] <= 8 and self.correct_rows(code)

    @classmethod
    def correct_rows(self, code):
        rows = [sum([
            int(y) if y.isdigit() else 1 for y in x]) for x in code.split('/')]
        return len(rows) == 8 and all(x == 8 for x in rows)
