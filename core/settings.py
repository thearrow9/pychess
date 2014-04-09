BOARD_SIZE = 8
Y_LABELS = 'abcdefgh'

ROOK_MOVE = {'left', 'right', 'up', 'down'}

BISHOP_MOVE = {}

KING_MOVE = ROOK_MOVE

START_POS_FEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'

PIECES = {'K': dict(label='King', points=1000, long_move=False,
               moves=[KING_MOVE], capture_moves=[],
               special_moves=[], start_pos = ['e1']),
          'Q': dict(label='Queen', points=9, long_move=True,
               moves=[KING_MOVE], capture_moves=[], special_moves=[],
               start_pos = ['d1']),
          'R': dict(label='Rook', points=5, long_move=True,
               moves=[ROOK_MOVE], capture_moves=[], special_moves=[],
               start_pos = ['a1', 'h1']),
          'B': dict(label='Bishop', points=3, long_move=True,
               moves=[BISHOP_MOVE], capture_moves=[], special_moves=[],
               start_pos = ['c1', 'f1']),
          'N': dict(label='Knight', points=2, long_move=False,
               moves=[], capture_moves=[], special_moves=[],
               start_pos = ['b1', 'g1']),
          'P': dict(label='Pawn', points=1, long_move=False,
               moves=[], capture_moves=[], special_moves=[],
               start_pos = ['a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2'])
         }
