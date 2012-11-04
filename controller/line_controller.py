__author__ = 'Atra'
from model.body import Line, LineSegment
from model.coord import GfxCoord, PhysCoord
from consts import SCREEN_HEIGHT
#class LineController(BaseController):
# todo make and use basecontroller
class LineController(object):

    def __init__(self, space):
        # todo world CAN NOT be used in this way. Do it properly
        # i.e. find a GOOD way to solve the whole space/world_objects problem...
        # best way is probably just to add world_objects to the custom Space,
        # and let all that shit be handled there instead of having to remember
        # to store everything in 2 different places.
        self.lines = []
        self.space = space

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
        self.space.world_objects.append(segment)
