import sys
sys.path.append('pychess')

import getopt
from game import Game
import settings

class ChessGame(Game):
    def __init__(self):
        try:
            options, args = getopt.getopt(sys.argv[1:], 'c:p:s:',
                ['color=', 'position=', 'strength='])
        except getopt.GetoptError:
            sys.exit()

        colors = strength = []
        fen = settings.START_POS_FEN

        for opt, val in options:
            if opt in ('-p', '--position'):
                fen = val
            elif opt in ('-c', '--color'):
                if 'w' in val: colors.append(0)
                if 'b' in val: colors.append(1)
            elif opt in ('-s', '--strength'):
                strength = [int(val)]

        super().__init__(fen)
        self.start_game(colors, *strength)


ChessGame()
