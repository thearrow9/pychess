import settings
import re

class Piece:
    def __init__(self, color, location):
        self.color = color
        self.moves = 0
        self.location = location
        self.in_play = True

    @property
    def char(self):
        return self.__class__.__name__

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

    def place(self, piece, color, notation):
        self[notation] = piece(color, notation)

    def place_id(self, piece, color, index):
        self.squares[index].piece = piece(
            color, self.index_to_string(index))

    def index_to_string(self, index):
        return '{}{}'.format(
            settings.Y_LABELS[index % settings.BOARD_SIZE],
                index // settings.BOARD_SIZE + 1)

    def str_to_index(self, notation):
        return settings.Y_LABELS.index(notation[0]) + \
            (int(notation[1]) - 1) * settings.BOARD_SIZE

    def opp_square(self, notation):
        return '{}{}'.format(notation[0], str(
            settings.BOARD_SIZE + 1 - int(notation[1])))

    def __getitem__(self, notation):
        return self.squares[self.str_to_index(notation)]

    def __setitem__(self, notation, item):
        self.squares[self.str_to_index(notation)].piece = item

class Game:
    def __init__(self):
        self.board = Board()
        self.reset()

    def get_all_in_play(self):
        return [x for x in self.board.squares \
            if x.is_occupied() and x.piece.in_play]

    def get_all_by(self, char, color):
        return list(self.__find(char, color))

    def get_first(self, char, color):
        return next(self.__find(char, color))

    def __find(self, char, color):
        return filter(lambda x: x.is_occupied() and \
            x.piece.char == char and x.piece.color == color,
                self.board.squares)

    def reset(self):
        self.parse_fen(settings.START_POS_FEN)

    def parse_fen(self, fen):
    #raise Error if invalid fen notation
        start_pos, self.to_move, self.possible_castle, \
            self.en_passant, self.since_capture, self.moves = fen.split(' ')
        i = 0
        for char in ''.join(start_pos.split('/')[::-1]):
            if char.isdigit():
                i += int(char)
            else:
                self.board.place_id(
                    CHESS_SET[char.upper()], int(char.islower()), i)
                i += 1

    def is_valid_fen(self, fen):
        return bool(re.match(
            '^({0}\/){{7}}{0} [wb] K?Q?k?q? (-|[a-z][36]) \d+ \d+'.\
                format('[rbnqkpRBNQKP1-8]{1,8}'), fen))
    #def move(square1, square2):
    #    self.board[square2].piece = self.board[square1].piece
    #    self.board[square1] = None
