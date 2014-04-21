import settings

class Square:
    def __init__(self, index):
        self.color = index % 2
        self.row = index // settings.BOARD_SIZE + 1
        self.col = index % settings.BOARD_SIZE
        self.piece = None

    def is_occupied(self):
        return self.piece is not None

    def __str__(self):
        return '{}{}'.format(settings.Y_LABELS[self.col], self.row)


class Board():
    def __init__(self):
        self.squares = [Square(i) for i in range(
            settings.BOARD_SIZE ** 2)]

    def place(self, piece, color, notation):
        self[notation] = piece(color, notation)

    def place_id(self, piece, color, index):
        self.squares[index].piece = piece(
            color, self.index_to_string(index))

    def index_to_string(self, index):
        return '{}{}'.format(
            settings.Y_LABELS[index % settings.BOARD_SIZE],
                index // settings.BOARD_SIZE + 1)


    def str_to_index(self, notation):
        return settings.Y_LABELS.index(notation[0]) + \
            (int(notation[1]) - 1) * settings.BOARD_SIZE

    def opp_square(self, notation):
        return '{}{}'.format(notation[0], str(
            settings.BOARD_SIZE + 1 - int(notation[1])))

    def __getitem__(self, notation):
        return self.squares[self.str_to_index(notation)]

    def __setitem__(self, notation, item):
        self.squares[self.str_to_index(notation)].piece = item
