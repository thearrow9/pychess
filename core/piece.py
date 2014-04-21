from notation import Notation

class Piece:
    def __init__(self, color, location):
        self.color = color
        self.made_moves = 0
        self.location = location
        self.in_play = True

    @property
    def char(self):
        return self.__class__.__name__

    def is_alias(self, piece):
        return self.color == piece.color

    def all_moves(self):
        notation = self.location
        x, y = Notation.str_to_coords(notation)

        moves = [[x * y[0], x * y[1]] for y in self.moves for x in range(1, 8)] \
            if self.long_move else self.moves

        if self.char == 'P' and self.color == 1:
            moves = [[-1 * y[0], -1 * y[1]] for y in moves]

        return set(Notation.coords_to_str([x + a, y + b]) for a, b in moves \
            if (x + a) in range(8) and (y + b) in range(8))
