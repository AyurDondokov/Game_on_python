import pygame
from properties import *
import logging as log


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos: tuple, groups: pygame.sprite.Group, path,
                 z: int = LAYERS['ground']):
        super().__init__(groups)
        self.z = z
        self.image = pygame.image.load(
            path).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.__hitbox = self.rect.copy()

    @property
    def hitbox(self):
        return self.__hitbox


class Trigger(Tile):
    """Tile c возможностью запуска func - функции"""

    def __init__(self,
                 pos: tuple,
                 groups: pygame.sprite.Group,
                 path,
                 func,
                 z: int = LAYERS['ground'],
                 ):
        super().__init__(pos, groups, path, z)
        self.trigger = True
        self.func = func

    def check(self):
        log.debug(f"funtion is {self.func}")
        self.func()
