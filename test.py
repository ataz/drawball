import math
import pymunk

class Human(object):

    def __init__(self, mass, race):
        self._mass = mass
        self._race = race

    @property
    def mass(self):
        return self._mass

    @mass.setter
    def mass(self, val):
        self._mass = math.pow(val, 2)


def incr(obj):
    print("Called.")
    return obj+3

m = [1,2,3,4]

map(incr, m)



atra = Human(10, "Persian")
print(atra.mass)

atra.mass = 3
print(atra.mass)



class Body(object):
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen

    def draw(self):
        raise NotImplementedError()

class Circle(Body):
    def draw(self):
        pass

class LineSegment(Body):
    def __init__(self, parent_screen, coord1, coord2):
        super().__init__(parent_screen)
        self.coord1 = coord1
        self.coord2 = coord2

    def draw(self):
#        pygame.draw.lines(self.parent_screen, THECOLORS['black'], False, [self.coord1, self.coord2], 5)
        print(self.parent_screen)

b = Body("Lol")
a = LineSegment("Hej", "a", "b")
a.draw()

l = []
def add(*args):
    l.extend(args)

def remove(*args):
    if isinstance(args, tuple):
        [l.remove(x) for x in args]


class Segment(object):
    def __init__(self, a, b):
        self.a = a

        self.b = b

segments = [Segment((1,2),(2,6)), Segment((2,6), (6,13)), Segment((6,13),(12,14))]
a = pymunk.Vec2d(1,3)
b = (1,3)
if a == b:
    print("yep")
print(segments)
res = []
def to_line(segments):
    for i in range(len(segments)):
        if res and segments[i].a == res[-1]:
            res.append(segments[i].b)
            continue
        res.extend((segments[i].a, segments[i].b))

to_line(segments)
print(res)



#add("a", 1,3)
#
#print(l)
#
#remove("a", 1)
#print(l)
