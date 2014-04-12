class Piece:
    def __init__(self, color, location):
        self.color = color
        self.made_moves = 0
        self.location = location
        self.in_play = True

    @property
    def char(self):
        return self.__class__.__name__

    def is_alias(self, piece):
        return self.color == piece.color
