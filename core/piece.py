from notation import Notation

class Piece:
    def __init__(self, color, location):
        self.color = color
        self.made_directions = 0
        self.location = location
        self.moves = self.attacks = set()

        if self.long_move:
            self.directions = [[x * y[0], x * y[1]] for y in self.directions \
                for x in range(1, 8)]

        if self.char == 'P' and self.color == 1:
            self.directions = [[-1 * y[0], -1 * y[1]] for y in self.directions]

    @property
    def in_play(self):
        return bool(self.location)

    @property
    def char(self):
        return self.__class__.__name__

    @property
    def code(self):
        return self.char.lower() if self.color else self.char

    def is_alias(self, piece):
        return self.color == piece.color

    def set_attacks(self, moves):
        if self.char == 'P':
            self.attacks = self.all_moves(self.directions[2:]) | moves - set(
                z for z in moves if self.location[0] == z[0])
        else:
            self.attacks = moves

    def all_moves(self, moves=set()):
        dirs = self.directions if not len(moves) else moves
        notation = self.location
        x, y = Notation.str_to_coords(notation)

        return set(Notation.coords_to_str(
            [x + a, y + b]) for a, b in dirs if (
            x + a) in range(8) and (y + b) in range(8))
