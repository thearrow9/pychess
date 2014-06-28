import subprocess
import re

class Engine:
    @classmethod
    def get_reply(self, fen, strength):
        output = str(subprocess.check_output(["sh", "bin/stockfish.sh", '{}'.format(fen), str(strength)]))
        move = re.search('bestmove (.+?) ', output).group(1)
        if len(move) > 4:
            move = move[:4] + '=' + move[-1].upper()
        return move[:2] + '-' + move[2:]
