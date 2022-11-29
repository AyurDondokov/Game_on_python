import pygame
from properties import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos: tuple, groups: pygame.sprite.Group):
        super().__init__(groups)
        self.image = pygame.image.load(
            'images/ground/ground.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
