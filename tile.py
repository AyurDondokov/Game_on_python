import pygame

from properties import *


class Tile(pygame.sprite.Sprite):
    """Основной класс для тайлов"""

    def __init__(self, pos: tuple, groups: pygame.sprite.Group, surface,
                 z: int = LAYERS['ground']):
        super().__init__(groups)
        self.z = z
        self.image = surface
        self.rect = self.image.get_rect(topleft=pos)
        self.__hitbox = self.rect.copy()

    @property
    def hitbox(self):
        return self.__hitbox


class NotTiledImage(Tile):
    def __init__(self, pos: tuple, groups: pygame.sprite.Group, surface, z: int = LAYERS['ground']):
        super().__init__(pos, groups,
                         surface, z)
        offset_y = pos[1] + TILE_SIZE
        self.rect = self.image.get_rect(bottomleft=(pos[0], offset_y))


class Trigger(Tile):
    """Tile c возможностью запуска скриптов"""

    def __init__(self,
                 pos: tuple,
                 groups: pygame.sprite.Group,
                 surface,
                 script,
                 z: int = LAYERS['ground']
                 ):
        super().__init__(pos, groups, surface, z)
        self.triggered = False
        self.script = script

    def check(self):
        # log.debug(f"funtion is {self.func}")
        if not self.triggered:
            self.script.execute()
            self.triggered = True
