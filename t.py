import pygame
import sys
import random
import pymunk
import logging

#log = logging.getLogger(__name__)

class log(object):
    @staticmethod
    def debug(arg):
        print(arg)

    @staticmethod
    def info(arg):
        print(arg)

class CircleJerk(object):
    def __init__(self, pos, size, color, width):
        """
        A basic circle class.
        :param pos: Initial position of the circle
        :type pos: tuple of int
        :param size: Size of the circle
        :type size: int
        :param color: Color of the circle
        :type color: tuple of int
        :param width: Line width
        :type width: int
        """
        self.x, self.y = pos
        self.size = size
        self.color = color
        self.width = width

        self.holder = None

    def draw(self):
        ret = pygame.draw.circle(screen, self.color, (self.x, self.y), self.size, self.width)
        self.holder = ret

    def move(self, direction, delta):
        NEGATIVE = direction.startswith("-")
        if "x" in direction.lower():
            self.x = self.x - delta if NEGATIVE else self.x + delta
            log.debug("Moved x-axis to %d" %self.x)
        else:
            self.y = self.y - delta if NEGATIVE else self.y + delta
            log.debug("Moved y-axis to %d" %self.y)
        self.draw()

    def info(self):
        log.info(dir(self.holder))

pygame.init()

width = 620
height = 340
screen = pygame.display.set_mode((width, height))

fps_clock = pygame.time.Clock()

def create_random_circle_set(n = 3):
    pos_arr = list()
    for i in range(n):
        pos_arr.append((random.randint(0, width), random.randint(0,height)))

    circles = (CircleJerk(pos, 10, (75,75,255), 3) for pos in pos_arr)
    return circles

objects = list()

def exit():
    pygame.quit()
    sys.exit()

delta = 2
once = True
while True:
    fps_clock.tick(60)
    pygame.display.set_caption("FPS: %.2f" % fps_clock.get_fps())
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                exit()
            elif event.key == pygame.K_RIGHT:
                [obj.move("+x", delta) for obj in objects]
            elif event.key == pygame.K_LEFT:
                [obj.move("-x", delta) for obj in objects]
            elif event.key == pygame.K_UP:
                [obj.move("-y", delta) for obj in objects]
            elif event.key == pygame.K_DOWN:
                [obj.move("+y", delta) for obj in objects]

    if len(objects) <= 0:
        [circle.draw() for circle in objects]
        circle_set = create_random_circle_set(1)
        objects.extend(circle_set)

    if once:
        objects[0].info()
        once = False

    pygame.display.flip()
