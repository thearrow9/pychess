import settings
import board
from notation import Notation
from piece import Piece
from validation import Validation
import errors

class GameBase:
    def __init__(self):
        self.board = board.Board()

    def parse_fen(self, fen):
        if not Validation.is_fen(fen):
            raise errors.InputError('Position requires two kings and no more than 8 pawns for each side')

        self.fen, to_move, self.castles, self.en_passant, self.halfmoves, \
            self.num_moves = fen.split(' ')
        self.num_moves = int(self.num_moves)
        self.board._arrange_pieces(self.fen)
        self.last_position = []

        self.to_move = 0 if to_move == 'w' else 1
        self.setup()

    def other_color(self, color):
        return 1 >> color

    def _switch_side(self):
       self.to_move = self.other_color(self.to_move)
       #if self.to_move:
       #    self.num_moves += 1

    def _encode_pieces(self):
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
        moves = set()
        for piece in pieces:
            moves.update(piece.moves)
        return moves

    def pieces_by_color(self, color):
        return [x.piece for x in self._find(
            ['K', 'Q', 'R', 'B', 'N', 'P'], color)]

    def pieces_in_play(self):
        return [x.piece for x in self.board.squares \
            if x.is_occupied()]

    def pieces_by(self, char, color):
        return [x.piece for x in self._find(char, color)]

    def pieces_by_char(self, char):
        white = [x.piece for x in self._find(char, 0)]
        black = [x.piece for x in self._find(char, 1)]
        return white + black

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
        return not self.is_under_attack(enemy_king)

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
        for alias in self.pieces_by_color(piece.color):
            if piece.location in alias.attacks: return True
        return False

    def is_under_attack(self, piece):
        return piece.location in self.all_attacks((self.other_color(piece.color)))


class PieceMove(PositionValidation):
    def __init__(self):
        super().__init__()

    def all_attacks(self, color):
        squares = set()
        pieces = self.pieces_by_color(color)
        for piece in pieces:
            squares.update(piece.attacks)
        return squares

    def promotion(self, char):
        pawns = [pawn for pawn in self.pieces_by_char('P') \
            if pawn.location[1] == '1' or pawn.location[1] == '8']
        if not len(pawns): return False
        pawn = pawns[0]
        new_piece = settings.CHESS_SET[char.upper()](
            pawn.color, pawn.location)

        self.board[pawn.location] = new_piece
        return True

    def _undo_last_move(self):
        if not len(self.last_position): return False
        last_position = self.last_position.pop()
        self.parse_fen(last_position)
        return True

    def set_en_passant(self, piece, location):
        if piece.char == 'P' and abs(
            Notation.row(location) - Notation.row(piece.location)) == 2:
                self.en_passant = location[0] + '6' if piece.color else location[0] + '3'
        else:
            self.en_passant = '-'

    def setup(self, legalization=True):
        for piece in self.pieces_in_play():
            piece.moves = set()
            piece.attacks, piece.all_moves = self._get_all_attacks(piece)

        if legalization:
            for piece in self.pieces_by_color(self.to_move):
                piece.moves = self._validated_moves(piece)

    def _get_all_attacks(self, piece):
        moves = self._get_moves(piece)
        attacks = self._get_pawn_captures(piece) if piece.char == 'P' \
            else moves
        all_moves = moves if piece.color == self.to_move else set()
        return [attacks, all_moves]

    def _validated_moves(self, piece, code=0):
        kings = self.pieces_by_char('K')
        color, opp_color = piece.color, self.other_color(piece.color)
        location = piece.location
        all_moves = set(move for move in piece.all_moves \
            if not self.board[move].is_occupied() or not piece.is_alias(
            self.piece_on(move)))
        enemies = self.pieces_by_color(opp_color)
        enemy_attacks = set()

        if piece.char == 'P':
            front_square = '{}{}'.format(
                location[0], Notation.row(location) + piece.directions[1][0][0])
            if piece.is_pawn_first_move() and self.board[front_square].is_occupied():
                all_moves -= set(move for move in all_moves if
                    move[0] == location[0])

            all_moves = set(move for move in all_moves \
                if move == self.en_passant or (
                    move[0] != location[0] and self.board[move].is_occupied()
                    and not piece.is_alias(self.piece_on(move))) or (
                    move[0] == location[0] and not self.board[move].is_occupied()))

        if piece.char == 'K':
            self.board[piece.location] = None
            for enemy in enemies:
                attacks, moves = self._get_all_attacks(enemy)
                enemy_attacks.update(attacks)
            self.board[location] = kings[color]
            all_moves -= set(
                move for move in all_moves if self.board[move].is_occupied() and
                    self.is_protected(self.piece_on(move)))

            return all_moves - enemy_attacks

        if not self.is_under_attack(kings[color]): return all_moves
        king_attackers = set(
            enemy for enemy in enemies if kings[color].location in enemy.attacks)

        if len(king_attackers) > 1: return set()
        if not len(king_attackers): return all_moves
        attacker = king_attackers.pop()
        return all_moves & Notation.squares_between(
            attacker.location, kings[color].location)

    def _get_pawn_captures(self, pawn):
        location = pawn.location
        x, y = Notation.str_to_coords(location)
        captures = [[c[0][0] + x, c[0][1] + y] for c in pawn.directions[2:]]
        captures = [Notation.coords_to_str(x) for x in captures]
        return set(x for x in captures if x)

    def _get_moves(self, piece):
        step = 0
        if piece.char == 'P' and not piece.is_pawn_first_move():
            step = 1

        dirs = piece.directions[step:]

        x, y = Notation.str_to_coords(piece.location)
        moves = protects = set()

        for direction in dirs:
            for coords in direction:
                new_x, new_y = coords[0] + x, coords[1] + y
                if new_x not in range(8) or new_y not in range(8): break
                square = Notation.coords_to_str([new_x, new_y])
                moves.update({square})
                if self.board[square].is_occupied(): break
        return moves

    def remove_piece(self, piece):
        self.board[piece.location] = None
        del piece

    def play(self, piece, location):
        self.set_en_passant(piece, location)
        self.last_position.append(self.save_position())
        start = str(piece.location)
        self.board[location] = piece
        self.board[start] = None
        self._switch_side()
        self.setup()

    def save_position(self):
        return '{} {} {} {} {} {}'.format(
            self._encode_pieces(), Notation.side_to_char(self.to_move),
            self.castles, self.en_passant, self.halfmoves, self.num_moves)


class Game(PieceMove):
    def __init__(self, fen=settings.START_POS_FEN):
        super().__init__()
        self.parse_fen(fen)

    def __repr__(self):
        return 'Position: {}'.format(
            ', '.join([str(x) for x in self.pieces_in_play()]))
