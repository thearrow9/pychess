import settings

class Piece:
    def __init__(self, name, label, points, directions):
        self.name = name
        self.label = label
        self.points = points
        self.directions = directions

pieces = {'King': {'points': 1000, 'directions': []}}

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
        self.squares = [Square(i) for i in range(settings.BOARD_SIZE ** 2)]

    def __getitem__(self, item):
        return ''
