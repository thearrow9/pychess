import settings
import board
from notation import Notation


class PieceMove():
    def __init__(self):
        self.board = board.Board()

    def piece_on(self, notation):
        return self.board[notation].piece

    def possible_moves(self, piece):
        moves = self.__get_moves(piece)
        return self.__pawn_moves(piece, moves) if piece.char == 'P' else moves

    def __pawn_moves(self, pawn, moves):
        color, location = pawn.color, pawn.location

        can_go_twice = (color == 1 and location[1] == '7') or (
            color == 0 and location[1] == '2')

        moves -= set(z for z in moves if z[0] != location[0] and \
            not self.board[z].is_occupied()) | set(
            z for z in moves if z[0] == location[0] and abs(
            int(z[1]) - int(location[1])) == 2 and not can_go_twice)

        return moves - set(z for z in moves if z[0] == location[0] \
            and self.board[z].is_occupied())

    def __get_moves(self, piece):
        return set(z for z in piece.all_moves() if not(
            self.board[z].is_occupied() and piece.is_alias(
            self.piece_on(z))) and self.__can_reach(piece, z))

    def __can_reach(self, piece, square):
        return self.__has_path(
            piece.location, square) if piece.long_move else True

    def __has_path(self, start, end):
        col_step = self.__get_step(ord(start[0]), ord(end[0]))
        row_step = self.__get_step(int(start[1]), int(end[1]))
        next_sq = start

        while True:
            next_sq = '{}{}'.format(chr(ord(next_sq[0]) + col_step),
                int(next_sq[1]) + row_step)
            if next_sq == end: return True
            if self.board[next_sq].is_occupied(): return False

    def __get_step(self, start, end):
        if end - start > 0: return 1
        if end - start < 0: return -1
        return 0


class Game(PieceMove):
    def __init__(self, fen=settings.START_POS_FEN):
        super().__init__()
        self.parse_fen(fen)

    def get_moves(self, piece):
#TODO
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
