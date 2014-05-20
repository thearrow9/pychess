import sys
sys.path.append('core')

from game import Game
import settings
import getopt

class ChessGame(Game):
    def __init__(self):
        try:
            options, args = getopt.getopt(sys.argv[1:], 'c:p:d:',
                ['color=', 'position=', 'depth='])
        except getopt.GetoptError:
            sys.exit()

        colors = depth = []
        fen = settings.START_POS_FEN

        for opt, val in options:
            if opt in ('-p', '--position'):
                fen = val
            elif opt in ('-c', '--color'):
                if 'w' in val: colors.append(0)
                if 'b' in val: colors.append(1)
            elif opt in ('-d', '--depth'):
                depth = [int(val)]
        #else:
        #    print('unhandled option')
        #    sys.exit()

        super().__init__(fen)
        self.start_game(colors, *depth)


z = ChessGame()
