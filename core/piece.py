from notation import Notation

class Piece:
    def __init__(self, color, location):
        self.color = color
        self.location = location
        self.moves = self.attacks = self.protects = self.captures = set()
        self.old_location = ''

        if self.char == 'P' and self.color == 1:
            self.directions = [[-1 * y[0], -1 * y[1]] for y in self.directions]

        if self.long_move:
            self.directions = list(map(lambda x: [[x[0] * z, x[1] * z] \
                for z in range(1, 8)], self.directions))
        else:
            self.directions = [[_] for _ in self.directions]

    def __repr__(self):
        return '{}{}'.format(self.code, self.location)

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
        return self.location[1] == ('7' if self.color else '2')

    def is_alias(self, piece):
        return self.color == piece.color

    #deprecated
    def set_attacks(self, moves):
        self.attacks = self.captures if self.char == 'P' else moves
