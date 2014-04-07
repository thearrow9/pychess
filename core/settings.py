BOARD_SIZE = 8
Y_LABELS = 'abcdefh'

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
