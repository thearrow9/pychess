import settings

class Piece:
    def __init__(self, color, location):
        self.color = color
        self.moves = 0
        self.location = location

    def is_alias(piece):
        return self.color == piece.color

CHESS_SET = dict((cls, type(cls, (Piece,), options)) \
    for cls, options in settings.PIECES.items())

class Square:
    def __init__(self, index):
        self.color = index % 2
        self.row = index // settings.BOARD_SIZE + 1
        self.col = index % settings.BOARD_SIZE
        self.piece = None

    def is_occupied(self):
        return self.piece is not None

    def __str__(self):
        return '{}{}'.format(settings.Y_LABELS[self.col], self.row)

class Board():
    def __init__(self):
        self.squares = [Square(i) for i in range(
            settings.BOARD_SIZE ** 2)]

    def place(self, piece, notation):
        self[self.notation_to_id(notation)] = piece

    def notation_to_id(self, notation):
        return settings.Y_LABELS.index(notation[0]) + \
            (int(notation[1]) - 1) * settings.BOARD_SIZE

    def opp_square(self, notation):
        return '{}{}'.format(notation[0], str(
            settings.BOARD_SIZE + 1 - int(notation[1])))

    def __getitem__(self, notation):
        return self.squares[self.notation_to_id(notation)]

    def __setitem__(self, index, item):
        self.squares[index].piece = item


class Game:
    def __init__(self):
        self.board = Board()
        self.reset()

    def select_all(self, label, color):
        return list(self.__find(label, color))

    def select_first(self, label, color):
        return next(self.__find(label, color))

    def __find(self, label, color):
        return filter(
            lambda x: x.is_occupied() and x.piece.label == label \
                and x.piece.color == color, self.board.squares)

    def reset(self):
        for piece in CHESS_SET.values():
            for notation in piece.start_pos:
                opp_piece_notation = self.board.opp_square(notation)
                self.board.place(piece(0, notation), notation)
                self.board.place(piece(1, opp_piece_notation), \
                    opp_piece_notation)

    def move(square1, square2):
        self.board[square2].piece = self.board[square1].piece
        self.board[square1] = None
