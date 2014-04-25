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

