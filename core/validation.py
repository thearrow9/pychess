import re

class Validation:
    @classmethod
    def is_fen(self, fen):
        code, *args = fen.split(' ')
        return bool(re.match(
            '^({0}\/){{7}}{0} [wb] K?Q?k?q? (-|[a-z][36]) \d+ \d+'. \
                format('[rbnqkpRBNQKP1-8]{1,8}'), fen)) \
                    and self.is_legal(code)

    @classmethod
    def is_legal(self, code):
        rules = {'K': [1], 'P': range(1, 9)}
        for char, rule in rules.items():
            if code.count(char) not in rule \
                or code.count(char.lower()) not in rule:
                return False
        return True
