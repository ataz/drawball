__author__ = 'Atra'
import pygame
import pymunk
import sys
from pymunk import Vec2d
from pygame.color import THECOLORS
from model.coord import PhysCoord, GfxCoord
from model.space import Space
from model.body import Ball, Body, LineSegment, Line
from controller.line_controller import LineController

from pygame.locals import *
import random
from queue import Queue, Empty, Full
from copy import deepcopy
from view.screen import PygameDisplay

class Game(object):
    # todo
    # Program should be structured in the following way:
    # Theoretically, a physics engine or a graphics engine should be
    # switchable. In other words, all object type classes should be
    # defined in my context, and then implemented using a picked
    # engine. That way, it will both keep the implementation
    # abstract, as well as gaining other OOP advantages and become
    # easier to separate.

    class States:
        INITIALIZED = 0
        RUNNING = 1
        PAUSED = 2
        STOPPED = 3

    def __init__(self, gravity=PhysCoord(0.0, -982.0), width=960, height=640, title="Drawball 0.1"):
        pygame.init()
        self.title = title
        self.FPS = 120

        self.segments = []

        self.width = width
        self.height = height
        self.clock = pygame.time.Clock()
        self.display = PygameDisplay()
        self.screen = self.display.set_mode(width, height)
        self.display.set_caption(title)
        self.space = Space(gravity)
        pygame.key.set_repeat(50,50)
        self.line_controller = LineController(self.space)

        self.event_queue = Queue()
        self.bgcolor = THECOLORS["white"]

        self.is_drawing = False
        self.state = self.States.INITIALIZED

    def start(self):
        self.state = self.States.RUNNING
        self.add_event(self.add_ball)
        while self.state == self.States.RUNNING:
            self._cycle()
            if self.state == self.States.STOPPED:
                break

        pygame.quit()
        sys.exit(0)

    def add_ball(self, position=None, mass=1, radius=14):
        # todo put in controller
        if not position:
            x = self.screen.get_width()/5
            y = self.screen.get_height()*0.8
            position = PhysCoord(x, y)

        ball = Ball(position, mass, radius=14)
        self.space.add(ball.body, ball.shape)
        self.space.world_objects.append(ball) # todo handle in controller

        return ball

    def draw_ball(self, ball, color=THECOLORS['black'], line_width=14):
        ball.draw(self.screen, color, line_width)
#        pos =
#        pos = self.make_coord(int(ball.body.position.x), int(ball.body.position.y))
#        pygame.draw.circle(self.screen._screen, color, pos, int(ball.radius), line_width)

#    def make_coord(self, x_or_pair, y=None):
#        # todo remove
#        if isinstance(x_or_pair, tuple):
#            x, y = x_or_pair
#        else:
#            x = x_or_pair
#            y = y
#        return (x, self.screen.get_height() - y)

    def add_event(self, event, *args):
        try:
            if args:
                ev = (event, args)
            else:
                ev = event
            self.event_queue.put(ev, block=False)
        except Full:
            return False

        return True

    def exec_event_queue(self):
        while not self.event_queue.empty():
            try:
                event = self.event_queue.get(block=False)
            except Empty:
                return
            if isinstance(event, tuple):
                func, args = event
                func(*args)
            else:
                event()

    def destroy(self, obj):
#        print("Destroying %s..." % str(obj))
        self.space.remove(obj.shape, obj.body)
#        print("World objects: %d" %len(self.world_objects))
        self.space.world_objects.remove(obj)

    def _cycle(self):
        self.exec_event_queue()
        self.screen.fill(self.bgcolor)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.state = self.States.STOPPED
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.state = self.States.STOPPED
                elif event.key == pygame.K_a:
                    self.add_event(self.add_ball)
                elif event.key == pygame.K_c:
                    # TODO implement
                    pass


            elif event.type == pygame.MOUSEBUTTONDOWN and not self.is_drawing:
#                assert(self.current_line is None)
                self.is_drawing = True
                self.line_controller.new_line(GfxCoord(event.pos))
#                self.add_event(self.line_controller.new_line(), GfxCoord(event.pos))
            elif event.type == pygame.MOUSEMOTION and self.is_drawing:
                self.line_controller.keep_drawing(GfxCoord(event.pos))
#                assert(self.current_line is not None)
#                self.add_event(self.draw_line, GfxCoord(event.pos))
#                gfx = GfxCoord(event.pos)
#                phys = gfx.to_phys(self.height)
#                print("Gfx: {}  Phys: {}".format(gfx, phys))
            elif event.type == pygame.MOUSEBUTTONUP:
                self.is_drawing = False
#                self.add_event(self.draw_line)

#        print(len(self.space.count_bodies()))
        for obj in self.space.world_objects:
            obj.draw(self.screen, THECOLORS['black'], 5)
            if isinstance(obj, Body) and obj.body.position.y < -50:
                self.destroy(obj)
#        if len(self.line_coord_arr) > 1:
#            pygame.draw.lines(self.screen, THECOLORS['black'], False, [self.make_coord(l) for l in self.line_coord_arr], 5)
#
#        for line in self.lines:
#            pygame.draw.lines(self.screen, THECOLORS['black'], False, [self.make_coord(l) for l in line], 5)


        self.space.step(1/self.FPS)
        self.display.set_caption("%s - FPS: %d" % (self.title, self.clock.get_fps()))
        self.display.flip() # TODO use update or flip?
        self.clock.tick(self.FPS)


if __name__ == "__main__":
#    g = Game(height=1000, width=1500)
    g = Game()
    g.start()
