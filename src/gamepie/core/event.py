import pygame
from .constants import SYS_CURSOR_ARROW
pygame.init()

class _Mouse:
    def __init__(self):
        self._mouse_x = 0
        self._mouse_y = 0
        self._mousewheel = 0
        
        self._left = False
        self._middle = False
        self._right = False
        self._cursor = SYS_CURSOR_ARROW
        self._int_mousewheel = 0
        
    def update(self, events):
        self._mouse_x, self._mouse_y = pygame.mouse.get_pos()
        self._left, self._middle, self._right = pygame.mouse.get_pressed()
        pygame.mouse.set_cursor(self._cursor)      
        self._int_mousewheel = self.getmouseweelint()
        for event in events:
            if event.type == pygame.MOUSEWHEEL:
                self._mousewheel = event.y

 
    def get(self):
        return [(self._mouse_x, self._mouse_y),self._left, self._middle, self._right, self._mousewheel] 
    def getmouseweelint(self):
        if self.mousewheel == 1:
            self._int_mousewheel += 1
            self.mousewheel = 0 
        elif self.mousewheel == -1:
            self._int_mousewheel -= 1
            self.mousewheel = 0 
        return self._int_mousewheel
    @property
    def int_mousewheel(self): return self._int_mousewheel
    @property
    def x(self): return self._mouse_x

    @property
    def y(self): return self._mouse_y

    @property
    def pos(self): return self._mouse_x, self._mouse_y

    @property
    def left(self): return self._left

    @property
    def middle(self): return self._middle

    @property
    def right(self): return self._right

    @property
    def mousewheel(self): return self._mousewheel
    @mousewheel.setter
    def mousewheel(self, value): 
        self._mousewheel = value
    @property
    def cursor(self): return self._cursor
    @cursor.setter
    def cursor(self, value): 
        self._cursor = value

    @property
    def camera(self): return self._camera
    @camera.setter
    def camera(self, value): 
        self._camera = value

class _Key:
    def __init__(self):
        self._keydown = False
        self._keyup = False
        self._any = False
        self._last_key = None
        self.char = None  
        self._pressed = pygame.key.get_pressed()

    def update(self, events):
        self.keydown = False
        self.keyup = False
        self.any = False
        self.char = None 

        for event in events:
            if event.type == pygame.KEYDOWN:
                self.keydown = True
                self.any = True
                self.last_key = event.key
                self.char = event.unicode  

            elif event.type == pygame.KEYUP:
                self.keyup = True
                self.any = True

        self._pressed = pygame.key.get_pressed()

    def get(self):
        return [self.char, self.keydown, self.keyup, self.any]

    def is_down(self, keyname: str):
        try:
            if keyname == "ctrl":
                return self._pressed[pygame.K_LCTRL] or self._pressed[pygame.K_RCTRL]
            else:
                keycode = pygame.key.key_code(keyname.lower())
                return self._pressed[keycode]
        except:
            return False

mouse = _Mouse()
key = _Key()
    
