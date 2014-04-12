import settings

class MoveIter:
    def top_left(self, notation):
        moves = set()

    def col_iter(self, notation, step):
        end_val = settings.FIRST_ORD - 1 if step < 0 \
            else settings.LAST_ORD + 1
        return iter(chr(x) for x in range(
            ord(notation[0]) + step, end_val, step))

    def row_iter(self, notation, step):
        end_val = settings.BOARD_SIZE + 1 if step > 0 else 0
        return iter(str(x) for x in range(
            int(notation[1]) + step, end_val, step))

    def diagonal_gen(self, iter1, iter2):
        for x in iter1: yield x + next(iter2)

