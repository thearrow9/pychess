class EvalLine:
    def __init__(self, string):
        parts = string.split(' ')
        self.moves, self.evaluation = ' '.join(parts[:-1]), float(parts[-1])
        self.first_move = parts[0]
        self.depth = self.moves.count(' ') + 1

    def __repr__(self):
        return '{} {}'.format(self.moves, self.evaluation)
