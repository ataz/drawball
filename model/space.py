__author__ = 'Atra'
import pymunk
from model.coord import PhysCoord

class Space(object):
    def __init__(self, gravity=PhysCoord(0.0, -982.0)):
        try:
            assert isinstance(gravity, PhysCoord)
        except AssertionError:
            print("Space class only takes PhysCoord arguments for gravity.")

        self._space = pymunk.Space()
        self._space.gravity = gravity
        self.gravity = gravity
        self.world_objects = []

    @property
    def bodies(self):
        return self._space.bodies

    @property
    def shapes(self):
        return self._space.shapes

    def remove(self, *objs, **world_objects):
        self._space.remove(*objs)
        user_objects = world_objects.get("world_objects")
        if user_objects:
            [self.world_objects.remove(obj) for obj in user_objects]

    #todo consider creating physic world controller where the world objects can be controlled.
    def add(self, *objs, **world_objects):
        self._space.add(*objs)
        user_objects = world_objects.get("world_objects")
        if user_objects:
            self.world_objects.extend(user_objects)

#    def add(self, *objs):
#        self._space.add(*objs)
#        self.world_objects.extend(objs)

    def count_bodies(self):
        return self._space.bodies

    def step(self, dt):
        return self._space.step(dt)

