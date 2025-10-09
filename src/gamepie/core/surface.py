import pygame
from .rect import Rect
class Surface:
    def __init__(self, size=(500, 500), position=(0,0), master=None, flags=(pygame.SRCALPHA,), surface=None):
        self.flags = flags if flags is not None else (pygame.SRCALPHA,)
        self.master = master
        
        if surface is not None:
            self.surface = surface
            self._w, self._h = surface.get_size()
        else:
            self._w, self._h = size
            combined_flags = 0
            for flag in self.flags:
                combined_flags |= flag
            self.surface = pygame.Surface((self._w, self._h), combined_flags)


    def fill(self, color=(255, 0, 0)):
        self.surface.fill(color)
        
    def __call__(self):
        return self.surface
    
    @property
    def size(self):
        return self.surface.get_size()

    @property
    def w(self):
        return self.surface.get_width()

    @property
    def h(self):
        return self.surface.get_height()

    @property
    def alpha(self):
        return self.surface.get_alpha()

    @alpha.setter
    def alpha(self, value):
        self.surface.set_alpha(value)

    @property
    def colorkey(self):
        return self.surface.get_colorkey()

    @colorkey.setter
    def colorkey(self, color):
        self.surface.set_colorkey(color)
    @property
    def rect(self):
        r = Rect(0, 0, self.w, self.h)
        return r

    @rect.setter
    def rect(self, value):
        self._rect = value

    def blit(self, source_surface, pos):
        self.surface.blit(source_surface, pos)

    def get_at(self, pos):
        return self.surface.get_at(pos)

    def set_at(self, pos, color):
        self.surface.set_at(pos, color)

    def copy(self):
        new_surface = self.surface.copy()
        return Surface(surface=new_surface)
    def __repr__(self):
        return repr(f"<Surface({self._w} ,{self._h})>")

    class _Transform:
        def __init__(self, outer):
            self.outer = outer  

        def rotate(self, angle):
            if angle != 0:
                rotated = pygame.transform.rotate(self.outer.surface, angle)
            else:
                rotated = self.outer.surface.copy()
            return Surface(surface=rotated)


        def scale(self, size, scale2x=False, smoothscale=False):
            if scale2x:
                scaled = pygame.transform.scale2x(self.outer.surface)
            elif smoothscale:
                scaled = pygame.transform.smoothscale(self.outer.surface, size)
            else:
                scaled = pygame.transform.scale(self.outer.surface, size)
            return Surface(surface=scaled)

        def rotozoom(self, angle, scale):
            result = pygame.transform.rotozoom(self.outer.surface, angle, scale)
            return Surface(surface=result)

        def flip(self, flip_x, flip_y):
            flipped = pygame.transform.flip(self.outer.surface, flip_x, flip_y)
            return Surface(surface=flipped)

        def chop(self, rect):
            chopped = pygame.transform.chop(self.outer.surface, rect)
            return Surface(surface=chopped)

    @property
    def transform(self):
        return self._Transform(self)
