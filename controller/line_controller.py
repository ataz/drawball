__author__ = 'Atra'
from model.body import Line, LineSegment
from model.coord import GfxCoord, PhysCoord
from consts import SCREEN_HEIGHT
#class LineController(BaseController):
# todo make and use basecontroller
class LineController(object):

    def __init__(self, space, world):
        self.lines = []
        self.space = space
        self.world = world

    def new_line(self, start_point=None, segments=None, radius=5):
        if start_point and isinstance(start_point, GfxCoord):
            start_point = start_point.to_phys(SCREEN_HEIGHT)
        line = Line(start_point, segments, radius)
        self.lines.append(line)

    def keep_drawing(self, new_point):
        if isinstance(new_point, GfxCoord):
            new_point = new_point.to_phys(SCREEN_HEIGHT)
        segment = self.lines[-1].add_point(new_point)
        self.space.add(segment.shape)
        self.world.append(segment)
