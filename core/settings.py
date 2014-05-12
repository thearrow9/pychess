from piece import Piece

BOARD_SIZE = 8
Y_LABELS = 'abcdefgh'

ROOK_MOVE_ON_CASTLE = {'g1': ['h1', 'f1'], 'c1': ['a1', 'd1'], 'g8': ['h8', 'f8'], 'c8': ['a8', 'd8']}

ROOK_DIR = [[-1, 0], [1, 0], [0, 1], [0, -1]]
BISHOP_DIR = [[1, 1], [1, -1], [-1, -1], [-1, 1]]
KNIGHT_DIR = [[1, 2], [1, -2], [-1, 2], [-1, -2], [2, -1], [2, 1], [-2, 1], [-2, -1]]
PAWN_DIR = [[2, 0], [1, 0], [1, 1], [1, -1]]

KING_DIR = BISHOP_DIR + ROOK_DIR

START_POS_FEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'

PIECES = {'K': dict(label='King', points=1000, long_move=False,
               directions=KING_DIR, strength=2),
          'Q': dict(label='Queen', points=9, long_move=True,
               directions=KING_DIR, strength=9),
          'R': dict(label='Rook', points=5, long_move=True,
               directions=ROOK_DIR, strength=5),
          'B': dict(label='Bishop', points=3, long_move=True,
               directions=BISHOP_DIR, strength=3),
          'N': dict(label='Knight', points=2.7, long_move=False,
               directions=KNIGHT_DIR, strength=2.7),
          'P': dict(label='Pawn', points=1, long_move=False,
               directions=PAWN_DIR, strength=1)
         }

CHESS_SET = dict((cls, type(cls, (Piece,), options)) \
    for cls, options in PIECES.items())
