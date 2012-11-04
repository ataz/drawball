import sys
import pygame
import pymunk
import random
from pygame.color import *
from pymunk.vec2d import Vec2d
from math import sin
import cmath
def to_pygame(p):
    """Small hack to convert pymunk to pygame coordinates"""
    return int(p.x), int(-p.y+600)

def add_ball(space):
    mass = 0.01
    radius = 1
    inertia = pymunk.moment_for_circle(mass/10, 0, radius)
    body = pymunk.Body(mass, inertia)
    x = random.randint(120,380)
#    x = 600/4
    x = random.randint(120,490)
    y = 600*1.05
    body.position = x, y
    shape = pymunk.Circle(body, radius)
    space.add(body, shape)
    return shape

def draw_ball(screen, ball):
    """
    :param ball: a Ball
    :type ball: a :class:`pymunk.Circle` object
    """
    pos = int(ball.body.position.x), 600 - int(ball.body.position.y)
    pygame.draw.circle(screen, (255,255,255), pos, int(ball.radius), 1)


def add_line(space, body, start, end, radius):
    line = pymunk.Segment(body, start, end, radius)
    space.add(line)
    return line

def add_line_from_body(space, body, length, radius):
    x, y = body.position
    first_endpoint = Vec2d(150,150)
    second_endpoint = Vec2d(-150,150)
    line = pymunk.Segment(body, first_endpoint, second_endpoint, radius)
    space.add(line)
    return line

def add_L(space):
    rotation_center_body = pymunk.Body()
    rotation_center_body.position = (300, 300)

    rotation_limit_body = pymunk.Body()
    rotation_limit_body.position = (200, 300)

    body = pymunk.Body(5, 1000)
    body.position = (300,300)
    l1 = add_line(space, body, start=(-150, 0), end=(255, 0), radius=5)
    l2 = add_line(space, body, start=(-150, 0), end=(-150, 50), radius=5)
#    l3 = add_line(space, body, start=(0, 100), end=(0, 400), radius=8)

#    l4 = add_line_from_body(space, body, 150, 5)

    rotation_center_joint = pymunk.PinJoint(body, rotation_center_body, (0,0), (0,0))
    joint_limit = 25
    rotation_limit_joint = pymunk.SlideJoint(body, rotation_limit_body, (-100,0), (0,0), 0, joint_limit)
#    space.add(l1, l2, body, rotation_center_joint, rotation_limit_joint)
    space.add(body, rotation_center_joint)
    return l1,l2

def draw_lines(screen, lines):
    for line in lines:
        body = line.body
        pv1 = body.position + line.a.rotated(body.angle) # 1
        pv2 = body.position + line.b.rotated(body.angle)
        p1 = to_pygame(pv1) # 2
        p2 = to_pygame(pv2)
        pygame.draw.lines(screen, THECOLORS["gray"], False, [p1,p2])


def mainloop():
    pygame.init()

    WIDTH = 600
    HEIGHT = 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pymunk test 0.1")
    clock = pygame.time.Clock()
    loop = True

    space = pymunk.Space()
    space.gravity = (0.0, -32.0)

    lines = add_L(space)
    balls = list()
    ticks_to_next_ball = 1


    TICK = 12
    ADD = 1
    gravity_tick = 12
    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                loop = False
        ticks_to_next_ball -= 1
        if ticks_to_next_ball <= 0:
            ticks_to_next_ball = 1
            ball_shape = add_ball(space)
            balls.append(ball_shape)

        screen.fill((0,0,0))

        for ball in balls:
#            pymunk.Body().apply_force()
            if random.randint(1,10) == 3:
                x = -0.1 if random.randint(0,1) == 1 else 0.1
                ball.body.apply_impulse((x,0))
#            ball.body.
            if ball.body.position.y > -10:
                draw_ball(screen, ball)
            else:
                space.remove(ball, ball.body)
                balls.remove(ball)

#        if random.randint(1,10):



#
#        gravity_tick += ADD
#        if gravity_tick >= TICK:
#            ADD = -1
#        elif gravity_tick <= (-1) * TICK:
#            ADD = 1
#
##            Better solution, rotate the gravity by radian angles instead.
#        space.gravity = (0.0+gravity_tick*60, -82.0+gravity_tick)


#        space.gravity.rotate(cmath.pi/20 - gravity_tick)

            # Keeping old solution commented out for reference.
#            space.gravity = (space.gravity[0] * (-1), space.gravity[1] * (-1))
#            gravity_tick = 350

        draw_lines(screen, lines)
        pygame.draw.circle(screen, THECOLORS["red"], (300,300), 5)
#        pygame.draw.circle(screen, THECOLORS["green"], (200,300), 25, 2)
        space.step(1/120)

        pygame.display.set_caption("FPS: %d" % (clock.get_fps()))

        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    mainloop()
    pygame.quit()
    sys.exit()





