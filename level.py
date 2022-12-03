import pygame
from properties import *
from tile import Tile
from player import Player

"""Отрисовка спрайтов на уровне"""


class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()

        self.visible_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()
        self.create_map()

        self.setup()

    def setup(self):
        self.player = Player((600, 300), self.visible_sprites)

    def create_map(self):
        for row_index, row in enumerate(MAP):
            for col_index, col in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                if col == 'x':
                    Tile((x, y), self.visible_sprites)

    def run(self, dt):
        self.visible_sprites.draw(self.display_surface)
        self.visible_sprites.update(dt)
