import settings

class Notation:
    @staticmethod
    def str_to_coords(notation):
        return [int(notation[1]) - 1,
            settings.Y_LABELS.index(notation[0])]

    @staticmethod
    def coords_to_str(coords):
        if not all(x in range(8) for x in coords): return False
        return '{}{}'.format(
            settings.Y_LABELS[coords[1]], int(coords[0]) + 1)

    @staticmethod
    def row(notation):
        return int(notation[1])

    @staticmethod
    def col(notation):
        return notation[0]

    @staticmethod
    def all_squares(inverted=False):
        order = range(8, 0, -1) if inverted else range(1, 9)
        return [x + str(y) for y in order for x in settings.Y_LABELS]

    @staticmethod
    def opp_square(notation):
        return '{}{}'.format(notation[0], str(
            settings.BOARD_SIZE + 1 - int(notation[1])))

    @staticmethod
    def squares_between(start, end):
        moves = {start, end}
        col_step = Notation.get_step(ord(end[0]), ord(start[0]))
        row_step = Notation.get_step(Notation.row(end), Notation.row(start))

        if start[0] == end[0]:
            return moves | set(end[0] + str(x) for x in range(
                Notation.row(start), Notation.row(end), row_step))

        if start[1] == end[1]:
            return moves | set(chr(x) + end[1] for x in range(
                ord(start[0]), ord(end[0]), col_step))

        cols = [chr(col) for col in range(ord(start[0]), ord(end[0]), col_step)]
        rows = [str(row) for row in range(Notation.row(start), Notation.row(end), row_step)]
        return moves | set(cols[i] + rows[i] for i in range(len(rows)))

    @staticmethod
    def get_step(a, b):
        if a > b: return 1
        if b > a: return -1
        return 0

    @staticmethod
    def side_to_char(index):
        return 'b' if index else 'w'
