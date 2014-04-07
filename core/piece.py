import settings

class Piece:
    def __init__(self, color):
        self.color = color
        self.moves = 0

    def is_alias(piece):
        return self.color == piece.color

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
        self.squares = [Square(i) for i in range(settings.BOARD_SIZE ** 2)]

    def place(self, piece, notation):
        self[self.notation_to_id(notation)] = piece

    def notation_to_id(self, notation):
        return settings.Y_LABELS.index(notation[0]) + \
            (int(notation[1]) - 1) * settings.BOARD_SIZE

    def opp_square(self, notation):
        return '{}{}'.format(notation[0], str(
            settings.BOARD_SIZE + 1 - int(notation[1])))

    def __getitem__(self, index):
        return self.squares[index]

    def __setitem__(self, index, item):
        self.squares[index].piece = item

ROOK_MOVE = [1, 8]

BISHOP_MOVE = [7, 9]

KING_MOVE = ROOK_MOVE + BISHOP_MOVE


PIECES = {'King': dict(label='K', points=1000, long_move=False,
                    moves=[KING_MOVE], capture_moves=[],
                    special_moves=[], start_pos = ['e1']),
          'Queen': dict(label='Q', points=9, long_move=True,
                    moves=[], capture_moves=[], special_moves=[],
                    start_pos = ['d1'])
         }

CHESS_SET = dict((cls, type(cls, (Piece,), options)) \
    for cls, options in PIECES.items())

class Game:
    def __init__(self):
        self.board = Board()
        self.reset()

    def reset(self):
        for piece in CHESS_SET.values():
            for notation in piece.start_pos:
                self.board.place(piece(0), notation)
                self.board.place(piece(1), \
                    self.board.opp_square(notation))

    def move(square1, square2):
        self.board[square2].piece = self.board[square1].piece
        self.board[square1] = None
