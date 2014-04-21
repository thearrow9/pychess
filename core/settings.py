from piece import Piece

BOARD_SIZE = 8
Y_LABELS = 'abcdefgh'
FIRST_ORD, LAST_ORD = ord(Y_LABELS[0]), ord(Y_LABELS[-1])

ROOK_MOVES = [[-1, 0], [1, 0], [0, 1], [0, -1]]
BISHOP_MOVES = [[1, 1], [1, -1], [-1, -1], [-1, 1]]
KNIGHT_MOVES = [[1, 2], [1, -2], [-1, 2], [-1, -2], [2, -1], [2, 1], [-2, 1], [-2, -1]]
PAWN_MOVES = [[1, 0], [2, 0], [1, 1], [1, -1]]

KING_MOVES = BISHOP_MOVES + ROOK_MOVES

START_POS_FEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'

PIECES = {'K': dict(label='King', points=1000, long_move=False,
               moves=KING_MOVES, capture_moves=[], special_moves=[]),
          'Q': dict(label='Queen', points=9, long_move=True,
               moves=KING_MOVES + BISHOP_MOVES, capture_moves=[], special_moves=[]),
          'R': dict(label='Rook', points=5, long_move=True,
               moves=ROOK_MOVES, capture_moves=[], special_moves=[]),
          'B': dict(label='Bishop', points=3, long_move=True,
               moves=BISHOP_MOVES, capture_moves=[], special_moves=[]),
          'N': dict(label='Knight', points=2, long_move=False,
               moves=KNIGHT_MOVES, capture_moves=[], special_moves=[]),
          'P': dict(label='Pawn', points=1, long_move=False,
               moves=PAWN_MOVES, capture_moves=[], special_moves=[])
         }

CHESS_SET = dict((cls, type(cls, (Piece,), options)) \
    for cls, options in PIECES.items())
