import settings
import board
from notation import Notation
from piece import Piece

class GameBase:
    def __init__(self):
        self.board = board.Board()

    def parse_fen(self, fen):
    #raise Error if invalid fen notation
        self.fen, to_move, self.castles, self.en_passant, self.halfmoves, \
            self.num_moves = fen.split(' ')
        self.num_moves = int(self.num_moves)
        self.board._arrange_pieces(self.fen)
        self.last_move = []

        self.to_move = 0 if to_move == 'w' else 1

    def _can_reach(self, piece, square):
        return self._has_path(
            piece.location, square) if piece.long_move else True

    def _has_path(self, start, end):
        col_step = self._get_step(ord(start[0]), ord(end[0]))
        row_step = self._get_step(int(start[1]), int(end[1]))
        next_sq = start

        while True:
            next_sq = '{}{}'.format(chr(ord(next_sq[0]) + col_step),
                int(next_sq[1]) + row_step)
            if next_sq == end: return True
            if self.board[next_sq].is_occupied(): return False

    def _get_step(self, start, end):
        if end - start > 0: return 1
        if end - start < 0: return -1
        return 0

    def other_color(self, color):
        return 1 >> color

    def _switch_side(self):
       self.to_move = self.other_color(self.to_move)
       #if self.to_move:
       #    self.num_moves += 1

    def _create_fen(self):
        fen = ''
        i = 0
        pieces = dict((p.location, p.code) for p in self.pieces_in_play())
        for square in Notation.all_squares(True):
            if square in pieces:
                if i > 0:
                    fen += str(i)
                    i = 0
                fen += pieces[square]
            else:
                i += 1
            if square[0] == 'h':
                if i > 0:
                    fen += str(i)
                    i = 0
                fen += '/'
        return fen[:-1]


class PieceSelector(GameBase):
    def __init__(self):
        super().__init__()

    def piece_on(self, notation):
        return self.board[notation].piece

    def moves_by_color(self, color):
        pieces = self.pieces_by_color(color)
        king = next(piece for piece in pieces if piece.char == 'K')

#TODO
        return

    def pieces_by_color(self, color):
        return [x.piece for x in self._find(
            ['K', 'Q', 'R', 'B', 'N', 'P'], color)]

    def pieces_in_play(self):
        return [x.piece for x in self.board.squares \
            if x.is_occupied() and x.piece.in_play]

    def pieces_by(self, char, color):
        return [x.piece for x in self._find(char, color)]

    def first_piece(self, char, color):
        return next(self._find(char, color)).piece

    def _find(self, char, color):
        return filter(lambda x: x.is_occupied() and \
            x.piece.char in char and x.piece.color == color,
                self.board.squares)

    def get_enemies(self, color):
        return self.pieces_by_color(self.other_color(color))


class PositionValidation(PieceSelector):
    def __init__(self):
        super().__init__()

    def is_valid_position(self):
        return self.are_kings_legally_placed()

    def are_kings_legally_placed(self):
        my_king = self.first_piece(['K'], self.to_move)
        enemy_king = self.first_piece(['K'], self.other_color(self.to_move))
        return enemy_king.location not in my_king.attacks and \
            not self.is_under_attack(enemy_king)

    def is_legal_short_castle(self, color):
        squares = ['f8', 'g8'] if color else ['f1', 'g1']
        king = self.first_piece(['K'], color)
        enemy_color = self.other_color(color)

        return not self.is_under_attack(king) and king.code in self.castles \
            and self.is_available(squares) and not self.is_attacked(
            squares[0], enemy_color) and not self.is_attacked(
            squares[1], enemy_color)

    def is_legal_long_castle(self, color):
        squares = ['c8', 'd8', 'b8'] if color else ['c1', 'd1', 'b1']
        king = self.first_piece(['K'], color)
        code = 'q' if color else 'Q'
        enemy_color = self.other_color(color)

        return not self.is_under_attack(king) and code in self.castles \
            and self.is_available(squares) and not self.is_attacked(
            squares[0], enemy_color) and not self.is_attacked(
            squares[1], enemy_color)

    def is_available(self, squares):
        for square in squares:
            if self.board[square].is_occupied(): return False
        return True

    def is_attacked(self, square, color):
        enemies = self.pieces_by_color(color)
        return any(square in enemy.attacks for enemy in enemies)

    def is_protected(self, piece):
        self.board[piece.location] = None
        flag = False
        aliases = self.pieces_by_color(piece.color)
        for alias in aliases:
            if piece.location in self.get_moves(alias): flag = True
        self.board[piece.location] = piece
        return flag

    def is_under_attack(self, piece):
        target = piece.location
        enemies = self.get_enemies(piece.color)
        for enemy in enemies:
            if target in enemy.attacks: return True
        return False


class PieceMove(PositionValidation):
    def __init__(self):
        super().__init__()

    def pawn_moves(self, pawn, all_moves):
        color, location = pawn.color, pawn.location
        moves = set(all_moves)

        can_go_twice = (color == 1 and location[1] == '7') or (
            color == 0 and location[1] == '2')

        moves -= set(z for z in moves if z[0] != location[0] and \
            not self.board[z].is_occupied() and z != self.en_passant) | set(
            z for z in moves if z[0] == location[0] and abs(
            int(z[1]) - int(location[1])) == 2 and not can_go_twice)

        return moves - set(z for z in moves if z[0] == location[0] \
            and self.board[z].is_occupied())

    def all_attacks(self, color):
        squares = set()
        pieces = self.pieces_by_color(color)
        for piece in pieces:
            squares.update(piece.attacks)
        return squares

    def record_moves(self, validation=True):
        kings = [self.first_piece(['K'], 0),
            self.first_piece(['K'], 1)]
        for piece in self.pieces_in_play():
            piece.moves = self.legal_moves(piece, kings[piece.color])

    def get_moves(self, piece):
        moves = set(z for z in piece.all_moves() if not(
            self.board[z].is_occupied() and piece.is_alias(
            self.piece_on(z))) and self._can_reach(piece, z))
        return self.pawn_moves(piece, moves) if piece.char == 'P' else moves

    def legal_moves(self, piece, king):
        valid_moves = self.get_moves(piece)
        piece.set_attacks(valid_moves)
        moves = set(valid_moves)
        enemies = self.get_enemies(piece.color)
        for move in moves:
            #self.try_move(piece, move)
            #self._undo_last_move()

            pass


        #FIXME bad method

        #if piece is not king and not self.is_under_attack(king):
        #    return valid_moves
        #if piece is king:
        #    moves = valid_moves - self.all_attacks(
        #        self.other_color(piece.color))
        #    return set(move for move in moves if \
        #        not self.board[move].is_occupied() or not self.is_protected(
        #        self.piece_on(move)))



        #for move in set(valid_moves):
        #    self._moved(piece, move)
        #    self.record_moves(False)
        #    if self.is_under_attack(king):
        #        valid_moves.remove(move)
        #    self._undo_last_move()

        return valid_moves

    def _undo_last_move(self):
        if not len(self.last_move): return False
        self.board[self.last_move['from']] = self.last_move['moved']
        self.board[self.last_move['to']] = self.last_move['taken']
        self._switch_side()
        return True

    def make_move(self, piece, location):
        self.try_move(piece, location)
        self.record_moves()

    def try_move(self, piece, location):
        if piece.char == 'P' and abs(
            Notation.row(location) - Notation.row(piece.location)) == 2:
                self.en_passant = location[0] + '6' if piece.color else location[0] + '3'
        else:
            self.en_passant = None
        self._moved(piece, location)
        self._switch_side()

    def _moved(self, piece, location):
        self.last_move = {'moved': piece, 'taken': self.piece_on(location),
            'from': piece.location, 'to': location}
        self.board[location] = piece
        self.board[piece.location] = None


class Game(PieceMove):
    def __init__(self, fen=settings.START_POS_FEN):
        super().__init__()
        self.parse_fen(fen)

