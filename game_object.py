import pygame


class GameObject:
    def __init__(self, x, y, w, h, speed=(0, 0)):
        self._bounds = pygame.Rect(x, y, w, h)
        self._speed = speed

    @property
    def x(self):
        return self._bounds.x

    @property
    def y(self):
        return self._bounds.y

    @property
    def left(self):
        return self._bounds.left

    @property
    def right(self):
        return self._bounds.right

    @property
    def top(self):
        return self._bounds.top

    @property
    def bottom(self):
        return self._bounds.bottom

    @property
    def width(self):
        return self._bounds.width

    @property
    def height(self):
        return self._bounds.height

    @property
    def center(self):
        return self._bounds.center

    @property
    def center_x(self):
        return self._bounds.centerx

    @property
    def center_y(self):
        return self._bounds.centery

    def draw(self, surface):
        pass

    def move(self, direction):
        self._bounds = self._bounds.move(*direction)

    def update(self):
        if self._speed == [0, 0]:
            return
        self.move(self._speed)
