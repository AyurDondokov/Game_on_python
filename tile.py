import pygame
from properties import *
import logging as log


class Tile(pygame.sprite.Sprite):
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

class Portal_components(Tile):
	def __init__(self, pos: tuple, groups: pygame.sprite.Group, z: int = LAYERS['ground']):
		super().__init__(pos, groups,
                 pygame.image.load('levels_data/graphics/decoration/ruined_portal/destroy_portal_components.png').convert_alpha(), z)
		offset_y = pos[1] + TILE_SIZE
		self.rect = self.image.get_rect(bottomleft = (pos[0],offset_y))

class Rocks(Tile):
	def __init__(self, pos: tuple, groups: pygame.sprite.Group, surface, z: int = LAYERS['ground']):
		super().__init__(pos, groups,
                 surface, z)
		offset_y = pos[1] + TILE_SIZE
		self.rect = self.image.get_rect(bottomleft = (pos[0],offset_y))

class Trigger(Tile):
    """Tile c возможностью запуска func - функции"""

    def __init__(self,
                 pos: tuple,
                 groups: pygame.sprite.Group,
                 surface,
                 func,
                 z: int = LAYERS['ground']
                 ):
        super().__init__(pos, groups, surface, z)
        self.trigger = True
        self.func = func

    def check(self):
        log.debug(f"funtion is {self.func}")
        self.func()
