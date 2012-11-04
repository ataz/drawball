__author__ = 'Atra'
import pygame

class Display(object):

    def fill(self, color):
        raise NotImplementedError

    def set_mode(self, width, height):
        raise NotImplementedError

    def set_caption(self, caption):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

    def flip(self):
        raise NotImplementedError

class PygameDisplay(Display):

    def __init__(self):
        self.width = None
        self.height = None
        self._display = pygame.display
        self._screen = None

    def fill(self, color):
        return self._screen.fill(color)

    def set_caption(self, caption):
        return self._display.set_caption(caption)

    def update(self):
        return self._display.update()

    def flip(self):
        return self._display.flip()

    def set_mode(self, width, height):
        self.width = width
        self.height = height
        self._screen = self._display.set_mode((width, height))
        return self._screen


