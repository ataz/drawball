import pymunk
import pygame
import consts
from model.coord import PhysCoord, get_midpoint

class Entity(object):
    """
    A physical object (could be a single body, a collection of bodies e.t.c.
    Basically, any dynamic and physical object which can be drawn on screen.
    """

    def draw(self, screen, color, line_width):
        raise NotImplementedError("Must be implemented in subclass")


class Line(Entity):
    """
    A collection of LineSegments, forming a line.
    """
    # TODO how to define the position of a line?
    def __init__(self, start_point=None, segments=None, radius=5):
        """
        :type segments: list
        """
        if not segments:
            assert isinstance(start_point, PhysCoord)
            self.start_point = start_point
            self.last_point = self.start_point

        self.radius = radius

        # self.segments is the list of LineSegment objects creating this line.
        self.segments = segments if segments else []
        # self._line is a list of unique tuples representing the coordinates which make the line.
        self._line = []
        if segments:
            self._make_line(segments)

    def add_point(self, point):
        """
        Add a point to this Line and return the resulting LineSegment
        """
        assert isinstance(point, PhysCoord)
        new_segment = LineSegment(self.last_point, point, self.radius)
        self._make_line(new_segment)
        return new_segment

    def _make_line(self, segments):
        def add_segment(segment):
            if self._line and segment.a == self._line[-1]:
                self._line.append(segment.b)
            else:
                self._line.extend((segment.a, segment.b))

            self.last_point = segment.b

        if isinstance(segments, list):
            for segment in segments:
                add_segment(segment)
        else:
            add_segment(segments)

    def add_segments(self, segments):
        """
        Add one or more segments to this Line.

        :type segments: list of model.body.LineSegment or model.body.LineSegment
        """
        if isinstance(segments, list):
            self.segments.extend(segments)
        else:
            self.segments.append(segments)

        self._make_line(segments)

    def draw(self, screen, color):
        line_width = self.radius
        if len(self._line) > 1:
            r = pygame.draw.lines(screen, color, False, [x.to_gfx(consts.SCREEN_HEIGHT) for x in self._line], line_width)


class Body(Entity):
    def __init__(self, position=None, mass=None, moment=None):
        self.body = pymunk.Body(mass, moment)
        if position:
            try:
                assert isinstance(position, PhysCoord)
                self.body.position = position
            except AssertionError:
                print("Supplied position is not an instance of PhysCoord")

    @property
    def position(self):
        return PhysCoord(self.body.position)


class Ball(Body):
    def __init__(self, position, mass, moment=None, radius=5):
        """
        :param position: The x,y coordinates of this Ball.
        :type position: model.coord.PhysCoord
        """
        self.mass = mass
        self.moment = pymunk.moment_for_circle(mass, 0, radius) if not moment else moment
        super().__init__(position, self.mass, self.moment)
        self.shape = pymunk.Circle(self.body, radius)

    # TODO should property be removed?

    def draw(self, screen, color, line_width):
        pos = self.position.to_gfx(consts.SCREEN_HEIGHT)
        # todo fix pygame dependency in class code?
        pygame.draw.circle(screen, color, pos, int(self.shape.radius), line_width)



class LineSegment(Body):
    """
    A line between 2 points
    """

    def __init__(self, start_point, end_point, radius=5):
        assert isinstance(start_point, PhysCoord)
        assert isinstance(end_point, PhysCoord)
        self.a = start_point
        self.b = end_point
        self.radius = radius
        super().__init__()
#        super().__init__(PhysCoord(get_midpoint(start_point, end_point)))
#        super().__init__(self.a)
        self.shape = pymunk.Segment(self.body, start_point, end_point, self.radius)

    def draw(self, screen, color, line_width=5):
        """
        Not recommended to use. Probably a better idea to use the draw method in the Line
        class instead and let pygame handle the draw optimizations.
        """
        pygame.draw.lines(screen, color, False, [self.a.to_gfx(consts.SCREEN_HEIGHT), self.b.to_gfx(consts.SCREEN_HEIGHT)], line_width)


if __name__ == "__main__":
    l1 = LineSegment(PhysCoord(1, 2), PhysCoord(2, 4))
    l2 = LineSegment(PhysCoord(2, 4), PhysCoord(3, 6))
    l3 = LineSegment(PhysCoord(3, 7), PhysCoord(5, 12))
    line = Line([l1, l2, l3])
    assert(line._line == [(1, 2), (2, 4), (3, 6), (3, 7), (5, 12)])
    print("All tests passed.")