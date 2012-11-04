import pymunk

class PhysCoord(pymunk.Vec2d):
    def __init__(self, x_or_pair=None, y=None):
        super().__init__(x_or_pair, y)

    def to_gfx(self, screen_height):
        """
        Translate these coordinates to gfx coordinates.
        """
        return GfxCoord((int(self.x), int(screen_height - self.y)))


class GfxCoord(tuple):
    def __new__(self, x_or_pair=None, y=None):
        if isinstance(x_or_pair, tuple):
            self.x, self.y = x_or_pair
        else:
            self.x = x_or_pair
            self.y = y

        return super().__new__(self, tuple((self.x, self.y)))


    def to_phys(self, screen_height):
        """
        Translate these coordinates to physics coordinates.
        """
        return PhysCoord(self.x, screen_height - self.y)


def get_midpoint(coord1, coord2):
    """
    Get the mid-point in coordinates between two points a and b.
    Requires that both have a .x and .y attribute.
    :type coord1: model.coord.GfxCoord or model.coord.PhysCoord
    :type coord2: model.coord.GfxCoord or model.coord.PhysCoord

    :rtype: tuple
    """
    return (coord1.x + coord2.x) / 2, (coord1.y + coord2.y) / 2