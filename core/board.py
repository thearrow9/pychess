import settings
from notation import Notation

class Square:
    def __init__(self, index, notation):
        self.index = index
        self.color = index % 2
        self.piece = None
        self.notation = notation

    def is_occupied(self):
        return self.piece is not None

    @property
    def row(self):
        return Notation.row(notation)

    @property
    def col(self):
        return self.notation[0]

    def __str__(self):
        return self.notation


class Board():
    def __init__(self):
        self.squares = [Square(i + 1, notation) for i, notation in enumerate(
            Notation.all_squares())]

    def place(self, piece, color, notation):
        self[notation] = piece(color, notation)

    def __getitem__(self, notation):
        return next(square for square in self.squares if notation in (
            square.notation, square.index))

    def __setitem__(self, notation, item):
        self[notation].piece = item
        if item is not None:
            item.location = notation

    def _arrange_pieces(self, fen):
        self.reset()
        i = 0
        squares = Notation.all_squares(True)
        for char in fen.replace('/', ''):
            if char.isdigit():
                i += int(char)
            else:
                self.place(
                    settings.CHESS_SET[char.upper()], int(
                    char.islower()), squares[i])
                i += 1

    def reset(self):
        for square in [x for x in self.squares if x.is_occupied()]:
            self[str(square)] = None
