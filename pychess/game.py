import settings
import board
from engine import Engine
from notation import Notation
from piece import Piece
from validation import Validation
from eval_line import EvalLine
import errors

class GameBase:
    def __init__(self):
        self.board = board.Board()
        self.analyse_board = board.Board()
        self.clear_history()
        self.rounder = EvalHelper.round_two_digits

    def parse_fen(self, fen):
        if not Validation.is_fen(fen):
            print(settings.MSG['invalid_fen'])
            return False

        self.fen, to_move, self.castles, self.en_passant, self.half_moves, \
            self.num_moves = fen.split(' ')
        self.num_moves = int(self.num_moves)
        self.half_moves = int(self.half_moves)
        self.board._arrange_pieces(self.fen)
        self.to_move = 0 if to_move == 'w' else 1
        self.setup()

    def other_color(self, color):
        return 1 - color

    def switch_side(self):
        if self.to_move: self.num_moves += 1
        self.to_move = self.other_color(self.to_move)
        self.setup()

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


class EvalHelper:
    @staticmethod
    def sum_points(pieces):
        return sum(piece.strength for piece in pieces)

    @staticmethod
    def sum_king_area_attacks(area, pieces):
        attackers = set(piece for piece in pieces if area & piece.moves)
        return len(attackers) * sum(piece.strength for piece in attackers)

    @staticmethod
    def sum_activity(pieces):
        return sum(piece.strength * len(piece.moves) for piece in pieces)

    @staticmethod
    def round_two_digits(number):
        return float('{0:.2f}'.format(number))


class GameEval(GameBase):
    def list_moves(self):
        return set('{}-{}'.format(piece.location,  moves) for piece in \
            self.pieces_by_color(self.to_move) for moves in piece.moves)

    def eval_material(self, white, black):
        whites_points = EvalHelper.sum_points(white)
        blacks_points = EvalHelper.sum_points(black)
        return self.rounder(whites_points - blacks_points)

    def eval_piece_activity(self, white, black):
        to_move = int(self.to_move)
        if to_move == 1: self.switch_side()
        whites_activity = EvalHelper.sum_activity(white)
        self.switch_side()
        blacks_activity = EvalHelper.sum_activity(black)
        self.to_move = to_move
        return self.rounder(whites_activity - blacks_activity)

    def eval_pawn_structure(self):
        #descrease double and isolated pawns
        #increase passed pawns
        pass

    def eval_kings_position(self, white, black):
        white_king = self.first_piece(['K'], 0)
        black_king = self.first_piece(['K'], 1)

        white_king_pts = EvalHelper.sum_king_area_attacks(
            white_king.attacks, white) - EvalHelper.sum_king_area_attacks(
            white_king.attacks, black)

        black_king_pts = EvalHelper.sum_king_area_attacks(
            black_king.attacks, black) - EvalHelper.sum_king_area_attacks(
            black_king.attacks, black)

        #TODO more precise evaluation

        return self.rounder(white_king_pts - black_king_pts)

    def eval_position(self):
        if self.is_checkmate(): return (self.to_move * 2 - 1) * 1000
        if self.is_draw(): return 0
        white = self.pieces_by_color(0)
        black = self.pieces_by_color(1)

        evaluation = 0
        evaluation += self.eval_kings_position(white, black) / 20
        evaluation += self.eval_piece_activity(white, black) / 300
        evaluation += self.eval_material(white, black)
        #evaluation += self.eval_pawn_structure(white, black)

        self.setup()
        return self.rounder(evaluation)

    def evaluate(self, depth = 3):
        VariationEval.set_position(self.save_position())
        all_nodes = [EvalLine(node) for node in VariationEval.evaluate(depth)]
        is_reverse = bool(1 - self.to_move)
        return sorted(all_nodes, key=lambda x: (x.evaluation), reverse=is_reverse)

class VariationEval:
    @classmethod
    def set_position(self, fen):
        self.game = Game(fen)
        self.start_fen = fen
        self.nodes = list(self.game.list_moves())
        self.report = set()

    @classmethod
    def evaluate(self, max_depth):
        for i, node in enumerate(list(self.nodes)):
            self.nodes[i] += self.play_node(node, max_depth)
            self.game.parse_fen(self.start_fen)
            self.game.clear_history()
        return self.nodes

    @classmethod
    def best_move(self, depth, path=''):
        if self.game.is_game_over():
            self.report.add(path + ' ' + str(self.game.eval_position()))
            return
        if depth == 1:
            evals = {}
            for move in self.game.list_moves():
                self.game.play(*move.split('-'))
                evals.update({move: self.game.eval_position()})
                self.game.undo_last_move()
            method = min if self.game.to_move else max
            best_val = method(evals.values())
            best_move = next(k for k, v in evals.items() if v == best_val)
            self.report.add(' ' + path + ' ' + best_move + ' ' + str(best_val))
            return

        for move in self.game.list_moves():
            self.game.play(*move.split('-'))
            self.best_move(depth - 1, path + move)
            self.game.undo_last_move()
        return


class PieceSelector(GameEval):
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
        return [x.piece for x in self.board.squares if x.is_occupied()]

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
    def is_valid_position(self):
        return self.are_kings_legally_placed()

    def are_kings_legally_placed(self):
        my_king = self.first_piece(['K'], self.to_move)
        enemy_king = self.first_piece(['K'], self.other_color(self.to_move))
        return not self.is_under_attack(enemy_king)

    def is_legal_castle(self, color, short_castle=True):
        king = self.first_piece(['K'], color)
        enemy_color = self.other_color(color)

        if short_castle:
            squares = ['f8', 'g8'] if color else ['f1', 'g1']
            code = king.code
        else:
            squares = ['c8', 'd8', 'b8'] if color else ['c1', 'd1', 'b1']
            code = 'q' if color else 'Q'

        return not self.is_under_attack(king) and code in self.castles \
            and self.are_available(squares) and not self.is_attacked(
            squares[0], enemy_color) and not self.is_attacked(
            squares[1], enemy_color)

    def are_available(self, squares):
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
        return piece.location in self.all_attacks(self.other_color(piece.color))


class PieceMove(PositionValidation):
    def all_attacks(self, color):
        squares = set()
        pieces = self.pieces_by_color(color)
        for piece in pieces:
            squares.update(piece.attacks)
        return squares

    def promotion(self, pawn, char):
        new_piece = settings.CHESS_SET[char.upper()](
            pawn.color, pawn.location)

        self.board[pawn.location] = new_piece
        return True

    def undo_last_move(self):
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
        attacks = self._get_pawn_captures(piece) if piece.char == 'P' else moves
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

            promoting_pieces = {'R', 'Q', 'B', 'N'}
            for move in set(all_moves):
                if move[1] == '1' or move[1] == '8':
                    all_moves.update(set('{}={}'.format(
                        move, x) for x in promoting_pieces ))
                    all_moves.remove(move)

        if piece.char == 'K':
            self.board[piece.location] = None
            for enemy in enemies:
                attacks, moves = self._get_all_attacks(enemy)
                enemy_attacks.update(attacks)
            self.board[location] = kings[color]
            all_moves -= set(
                move for move in all_moves if self.board[move].is_occupied() and
                    self.is_protected(self.piece_on(move)))

            if self.is_legal_castle(piece.color):
                all_moves.add('G8') if piece.color else all_moves.add('G1')

            if self.is_legal_castle(piece.color, False):
                all_moves.add('C8') if piece.color else all_moves.add('C1')

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

    def play(self, start, end):
        piece = self.piece_on(start)
        if piece is None:
            print(settings.MSG['no_piece_on_sq'])
            return False
        if piece.color != self.to_move:
            print(settings.MSG['opp_piece'])
            return False
        if end not in piece.moves and end.upper() not in piece.moves:
            print(settings.MSG['illegal_move'])
            return False
        self.old_en_passant = str(self.en_passant)
        self.last_position.append(self.save_position())

        end, *prom = end.split('=')
        self.make_the_move(piece, end.lower())
        if prom: self.promotion(piece, prom[0])

        self.switch_side()

    def simple_move(self, piece, location):
        start = str(piece.location)

        self.board[location] = piece
        self.board[start] = None

    def make_the_move(self, piece, location):
        self.set_en_passant(piece, location)

        if location.upper() in piece.moves:
            rook_moves = settings.ROOK_MOVE_ON_CASTLE[location]
            self.simple_move(self.piece_on(rook_moves[0]), rook_moves[1])

        self.half_moves = 0 if self.board[location].is_occupied() \
            or piece.char == 'P' else self.half_moves + 1

        self.simple_move(piece, location)
        self.remove_victim_on_en_passant(piece, location)
        self.disable_castles(piece)

    def disable_castles(self, piece):
        if piece.color:
            castles = 'kq'
            rank = 8
        else:
            castles = 'KQ'
            rank = 1

        if self.castles == '-' or castles not in self.castles: return

        if piece.char == 'K':
            self.castles = self.castles.replace(castles[0], '')
            self.castles = self.castles.replace(castles[1], '')

        rook_locations = ['h' + str(rank), 'a' + str(rank)]

        if piece.old_location == rook_locations[0] or piece.location == rook_locations[0]:
            self.castles = self.castles.replace(castles[0], '')

        if piece.old_location == rook_locations[1] or piece.location == rook_locations[1]:
            self.castles = self.castles.replace(castles[1], '')

        if not self.castles: self.castles = '-'

    def remove_victim_on_en_passant(self, piece, location):
        if location == self.old_en_passant and piece.char == 'P':
            row = 4 if piece.color else 5
            self.board['{}{}'.format(self.old_en_passant[0], row)] = None

    def save_position(self):
        return '{} {} {} {} {} {}'.format(
            self._encode_pieces(), Notation.side_to_char(self.to_move),
            self.castles, self.en_passant, self.half_moves, self.num_moves)


class Game(PieceMove):
    def __init__(self, fen=settings.START_POS_FEN):
        super().__init__()
        self.parse_fen(fen)

    def clear_history(self):
        self.last_position = []

    def is_stalemate(self):
        king = self.first_piece(['K'], self.to_move)
        return self.has_no_moves() and not self.is_under_attack(king)

    def has_no_moves(self):
        return not len(self.list_moves())

    def is_checkmate(self):
        king = self.first_piece(['K'], self.to_move)
        return self.has_no_moves() and self.is_under_attack(king)

    def is_fifty_move_draw(self):
        return self.half_moves >= 50

    def is_treefold_draw(self):
        positions = [''.join(x.split(' ')[:-2]) for x in self.last_position]
        return any(positions.count(x) >= 3 for x in set(positions))

    def is_impossible_to_checkmate(self):
        pieces = self.pieces_in_play()
        total_points = sum(piece.points for piece in pieces)
        return len(pieces) == 2 or (
            len(pieces) == 3 and 2001 < total_points <= 2003)

    def is_draw(self):
        if self.is_checkmate(): return False
        return self.is_stalemate() or self.is_impossible_to_checkmate() \
            or self.is_treefold_draw() or self.is_fifty_move_draw()

    def is_game_over(self):
        return self.is_draw() or self.is_checkmate()

    def set_CPU_params(self, colors, strength=2):
        self.cpu = {'color': colors, 'strength': strength}

    #test method
    def start_game(self, color, strength):
        self.set_CPU_params(color, strength)
        while True:
            if self.is_game_over():
                if self.is_draw():
                    msg = 'Draw by '
                    if self.is_stalemate():
                        msg += 'stalemate'
                    elif self.is_treefold_draw():
                        msg += 'treefold repetition'
                    else:
                        msg += '50 move rule'
                else:
                    msg = 'White' if self.to_move else 'Black'
                    msg += ' wins'
                print('Game over! ' + msg)
                break

            if self.to_move in self.cpu['color']:
                print('CPU is calculating...')
                best_line = Engine.get_reply(self.save_position(), self.cpu['strength'])
                print("...and plays " + best_line)
                self.play(*best_line.split('-'))
            else:
                print(self)
                cmd = input(settings.MSG['your_turn'])
                if Validation.is_move(cmd):
                    self.play(*cmd.split('-'))
                else:
                    print(settings.MSG['invalid_move'])


    def __repr__(self):
        output = "\n"
        for char in settings.Y_LABELS:
            output += char + ' '
        output += "\n"
        for square in Notation.all_squares(True):
            piece = self.piece_on(square)
            if piece is None:
                output += settings.UNICODE_PIECES['blank']
            else:
                output += settings.UNICODE_PIECES[piece.code]

            output += " "

            if square.startswith('h'):
                output += "{}\n".format(square[1])

        return output
