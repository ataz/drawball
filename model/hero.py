__author__ = 'Atra'
import pymunk

class HeroModel(object):
    """
    The main hero of the game (a ball).

    """

    def __init__(self, position, mass, inertia):
        self._body = pymunk.Body(mass, inertia)

    def accelerate(self, a):
        pass

    def jump(self, a):
        """
        :param a: Acceleration to jump with
        :type a: float
        """
        pass

    def run(self):
        """
        If it's lol w print "haha"
        """
        for i in xrange(300):
            [setattr("lol?")]



