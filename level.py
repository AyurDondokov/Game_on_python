import pygame
from properties import *
from tile import Tile
from player import Player
import logging
log = logging.getLogger(__name__)
"""Отрисовка спрайтов на уровне"""


class Level:
    def __init__(self):
        log.info('Level class intialization')
        self.display_surface = pygame.display.get_surface()

        self.all_sprites = CameraGroup()
        self.collision_sprites = pygame.sprite.Group()
        self.create_map()

        self.setup()

    def setup(self):
        """Загрузка важных объектов на уровне"""
        self.player = Player((600, 300), self.all_sprites, ((20, 20), (0, 0)), self.collision_sprites)

    def create_map(self):
        for row_index, row in enumerate(MAP):
            for col_index, col in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                if col == 'x':
                    Tile((x, y), [self.all_sprites, self.collision_sprites])

    def run(self, dt):
        self.all_sprites.custom_draw(self.player)
        self.all_sprites.update(dt)


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

        self.display_surf = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - SCREEN_WIDTH / 2
        self.offset.y = player.rect.centery - SCREEN_HEIGHT / 2

        for layer in LAYERS.values():
            for sprite in self.sprites():
                if sprite.z == layer:
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    self.display_surf.blit(sprite.image, offset_rect)
