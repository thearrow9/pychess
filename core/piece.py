import settings
import re

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

class MoveIter:
    def top_left(self, notation):
        moves = set()

    def col_iter(self, notation, step):
        end_val = settings.FIRST_ORD - 1 if step < 0 \
            else settings.LAST_ORD + 1
        return iter(chr(x) for x in range(
            ord(notation[0]) + step, end_val, step))

    def row_iter(self, notation, step):
        end_val = settings.BOARD_SIZE + 1 if step > 0 else 0
        return iter(str(x) for x in range(
            int(notation[1]) + step, end_val, step))

    def diagonal_gen(self, iter1, iter2):
        for x in iter1: yield x + next(iter2)


class MoveRule(MoveIter):
    def __init__(self):
        self.board = Board()

    def bishop_moves(self, notation):
        moves = []
        direction = 1 if pawn.color == 0 else -1




    def piece_on(self, notation):
        return self.board[notation].piece

    def rook_moves(self, iterator, notation, step=1):
        moves = set()
        for item in iterator(notation, step):
            square = item + notation[1] if item.islower() \
                else notation[0] + item
            is_end = self.__piece_on_way(self.piece_on(notation), square)
            if is_end: return moves | is_end[0]
            moves.add(square)
        return moves

    def __piece_on_way(self, piece, square):
        if self.board[square].is_occupied():
            if piece.is_alias(self.piece_on(square)):
                return [set()]
            return [{square}]
        return False

    def left(self, notation):
        return self.rook_moves(self.col_iter, notation, -1)

    def right(self, notation):
        return self.rook_moves(self.col_iter, notation)

    def up(self, notation):
        return self.rook_moves(self.row_iter, notation)

    def down(self, notation):
        return self.rook_moves(self.row_iter, notation, -1)

    def top_left(self, notation):
        return {x for x in self.diagonal_gen(
            self.col_iter(notation, -1), self.row_iter(notation, 1))}


class Game(MoveRule):
    def __init__(self, fen=settings.START_POS_FEN):
        super().__init__()
        self.parse_fen(fen)

    def get_moves(self, piece):
        return

    def pieces_by_color(self, color):
        return self.__find(['K', 'Q', 'R', 'B', 'N', 'P'], color)

    def pieces_in_play(self):
        return [x.piece for x in self.board.squares \
            if x.is_occupied() and x.piece.in_play]

    def pieces_by(self, char, color):
        return [x.piece for x in self.__find(char, color)]

    def first_piece(self, char, color):
        return next(self.__find(char, color)).piece

    def __find(self, char, color):
        return filter(lambda x: x.is_occupied() and \
            x.piece.char in char and x.piece.color == color,
                self.board.squares)

    def reset_board(self):
        for square in filter(lambda x: x.is_occupied(), self.board.squares):
            self.board[str(square)].piece.location = \
                self.board[str(square)] = None



    def parse_fen(self, fen):
    #raise Error if invalid fen notation
        self.reset_board()
        start_pos, *self.options = fen.split(' ')
        i = 0
        for char in ''.join(start_pos.split('/')[::-1]):
            if char.isdigit():
                i += int(char)
            else:
                self.board.place_id(
                    CHESS_SET[char.upper()], int(char.islower()), i)
                i += 1

        self.to_move = 0 if self.options[0] == 'w' else 1

    def __switch_side(self):
       self.to_move = (self.to_move + 1) % 2


class Validation:
    @classmethod
    def is_fen(self, fen):
        code, *args = fen.split(' ')
        return bool(re.match(
            '^({0}\/){{7}}{0} [wb] K?Q?k?q? (-|[a-z][36]) \d+ \d+'. \
                format('[rbnqkpRBNQKP1-8]{1,8}'), fen)) \
                    and self.correct_pieces(code)

    @classmethod
    def correct_pieces(self, code):
        rules = {'K': [1], 'P': range(1, 9)}
        for char, rule in rules.items():
            if code.count(char) not in rule \
                or code.count(char.lower()) not in rule:
                return False
        return True

