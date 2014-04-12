import settings
import board
from moveiter import MoveIter
from piece import Piece

class MoveRule(MoveIter):
    def __init__(self):
        self.board = board.Board()

    def bishop_moves(self, notation, col_step, row_step):
        moves = set()
        for square in self.diagonal_gen( \
            self.col_iter(notation, col_step), \
                self.row_iter(notation, row_step)):
            is_end = self.piece_on_way(self.piece_on(notation), square)
            if is_end: return moves | is_end[0]
            moves.add(square)
        return moves

    def piece_on(self, notation):
        return self.board[notation].piece

    def rook_moves(self, iterator, notation, step=1):
        moves = set()
        for item in iterator(notation, step):
            square = item + notation[1] if item.islower() \
                else notation[0] + item
            is_end = self.piece_on_way(self.piece_on(notation), square)
            if is_end: return moves | is_end[0]
            moves.add(square)
        return moves

    def piece_on_way(self, piece, square):
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

    def up_left(self, notation):
        return self.bishop_moves(notation, -1, 1)

    def up_right(self, notation):
        return self.bishop_moves(notation, 1, 1)

    def down_left(self, notation):
        return self.bishop_moves(notation, -1, -1)

    def down_right(self, notation):
        return self.bishop_moves(notation, 1, -1)


class PieceMove(MoveRule):
    def __init__(self):
        super().__init__()

    def possible_moves(self, piece):
        methods = [getattr(self, x) for x in piece.moves]
        return methods[0](piece.location)

    def rook(self, notation):
        return self.left(notation) | self.right(notation) | \
            self.up(notation) | self.down(notation)

    def bishop(self, notation):
        return self.up_left(notation) | self.up_right(notation) | \
            self.down_left(notation) | self.down_right(notation)


class Game(PieceMove):
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
                    settings.CHESS_SET[char.upper()], int(char.islower()), i)
                i += 1

        self.to_move = 0 if self.options[0] == 'w' else 1

    def __switch_side(self):
       self.to_move = (self.to_move + 1) % 2
