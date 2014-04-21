import settings

class Notation:
    @classmethod
    def str_to_coords(self, notation):
        return [int(notation[1]) - 1,
            settings.Y_LABELS.index(notation[0])]

    @classmethod
    def coords_to_str(self, coords):
        return '{}{}'.format(
            settings.Y_LABELS[coords[1]], int(coords[0]) + 1)
