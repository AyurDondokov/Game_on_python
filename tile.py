import pygame
from properties import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos: tuple, groups: pygame.sprite.Group, path,
                 z: int = LAYERS['ground']):
        super().__init__(groups)
        self.z = z
        self.image = pygame.image.load(
            path).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.copy()
