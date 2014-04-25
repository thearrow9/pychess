from notation import Notation

class Piece:
    def __init__(self, color, location):
        self.color = color
        self.made_directions = 0
        self.location = location
        self.moves = self.attacks = set()
        self.captures = set()

        self.directions_ = self.directions[:]
        if self.char == 'P' and self.color == 1:
            self.directions_ = [[-1 * y[0], -1 * y[1]] for y in self.directions_]

        if self.long_move:

            self.directions_ = list(map(lambda x: [[x[0] * z, x[1] * z] \
                for z in range(1, 8)], self.directions))

            self.directions = [[x * y[0], x * y[1]] for y in self.directions \
                for x in range(1, 8)]
        else:
            self.directions_ = [[_] for _ in self.directions_]

        if self.char == 'P' and self.color == 1:
            self.directions = [[-1 * y[0], -1 * y[1]] for y in self.directions]

    def __repr__(self):
        return '{} {} on {}'.format(self.color_name, self.label, self.location)

    @property
    def color_name(self):
        return 'black' if self.color else 'white'

    @property
    def in_play(self):
        return bool(self.location)

    @property
    def char(self):
        return self.__class__.__name__

    @property
    def code(self):
        return self.char.lower() if self.color else self.char

    def is_pawn_first_move(self):
        if self.char != 'P': return False
        rank = '7' if self.color else '2'
        return self.location[1] == rank

    def is_alias(self, piece):
        return self.color == piece.color

    def _set_attacks(self):
        if self.char == 'P':
            self.attacks = self.all_moves(self.directions_[2:]) | self.moves - set(
                z for z in self.moves if self.location[0] == z[0])
        else:
            self.attacks = self.moves

    def set_attacks(self, moves):
        if self.char == 'P':
            self.attacks = self.all_moves(self.directions[2:]) | moves - set(
                z for z in moves if self.location[0] == z[0])
        else:
            self.attacks = moves

    def setup(self, moves):
        self.attacks = self.captures if self.char == 'P' else moves
        self.moves = moves

    def all_moves(self, moves=set()):
        dirs = self.directions if not len(moves) else moves
        notation = self.location
        x, y = Notation.str_to_coords(notation)

        return set(Notation.coords_to_str(
            [x + a, y + b]) for a, b in dirs if (
            x + a) in range(8) and (y + b) in range(8))
