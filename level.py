import pygame
from properties import *
from tile import Tile
from player import Player
import logging
from character import NPC
log = logging.getLogger(__name__)
"""Отрисовка спрайтов на уровне"""


class Level:
    def __init__(self, level_map):
        log.info('Level class intialization')
        self.display_surface = pygame.display.get_surface()

        self.map = level_map
        self.all_sprites = CameraGroup()
        self.collision_sprites = pygame.sprite.Group()
        self.interactable_sprites = pygame.sprite.Group()
        self.create_map()

        self.setup()

    def setup(self):
        """Загрузка важных объектов на уровне"""
        self.test_npc = NPC(
            position=(500, 600),
            sprite_group=[self.all_sprites,
                          self.collision_sprites, self.interactable_sprites],
            name='Ayur',
            dialog_replicas=('Ayur:Hello', 'Ayur:My name is Ayur', 'Ayur:Its first dialog in game'))
        self.player = Player((600, 300), self.all_sprites,
                             self.collision_sprites, self.interactable_sprites)

    def create_map(self):

        for row_index, row in enumerate(self.map):
            for col_index, col in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                if col == 'x':
                    Tile((x, y), self.all_sprites, 'images/ground/sand.png')
                if col == 's':
                    Tile((x, y), self.all_sprites, 'images/ground/sand2.png')
                if col == "c":
                    Tile(
                        (x, y), [self.all_sprites, self.collision_sprites], 'images/ground/cactus.png')

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
                if 'back' in list(LAYERS.keys())[sprite.z] or 'forward' in list(LAYERS.keys())[sprite.z]:
                    if sprite.rect.centery > player.rect.centery:
                        sprite.z = LAYERS['forward_' +
                                          list(LAYERS.keys())[sprite.z].split('_')[1]]
                    else:
                        sprite.z = LAYERS['back_' +
                                          list(LAYERS.keys())[sprite.z].split('_')[1]]
                if sprite.z == layer:
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    self.display_surf.blit(sprite.image, offset_rect)
