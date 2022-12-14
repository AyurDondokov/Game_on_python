import pygame
from properties import *
from tile import Tile, Trigger
from player import Player
import logging
from character import NPC
import sys
log = logging.getLogger(__name__)
"""Отрисовка спрайтов на уровне"""


class Level:
    def __init__(self, level_map, current_level, lvl_go_to):
        log.info(f'Level class intialization')
        self.display_surface = pygame.display.get_surface()

        # для перемещения между уровнями
        self.cur_lvl = current_level
        self.lvl_to = lvl_go_to

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

    def create_map(self):

        for row_index, row in enumerate(self.map):
            for col_index, col in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                if col == 'x':
                    Tile((x, y), self.all_sprites, 'images/ground/sand.png')
                if col == 's':
                    Tile((x, y), self.all_sprites, 'images/ground/sand2.png')
                if col == 't':
                    Trigger((x, y), [self.all_sprites, self.collision_sprites],
                            'images/ground/trigger.png', lambda: self.cur_lvl(self.lvl_to))
                if col == "c":
                    Tile(
                        (x, y), [self.all_sprites, self.collision_sprites], 'images/ground/cactus.png')
                if col == "p":
                    self.player = Player((x, y), self.all_sprites,
                                         self.collision_sprites, self.interactable_sprites)

    def run(self, dt):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        self.all_sprites.custom_draw(self.player)
        self.all_sprites.update(dt)


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

        self.display_surf = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player):
        """Отрисовка персонажа всегда в центре. Метод  камеры."""
        self.offset.x = player.rect.centerx - SCREEN_WIDTH / 2
        self.offset.y = player.rect.centery - SCREEN_HEIGHT / 2

        for layer in LAYERS.values():
            for sprite in self.sprites():
                if 'back' in list(LAYERS.keys())[sprite.z] or 'forward' in list(LAYERS.keys())[sprite.z]:
                    # нужно для правильного накладывания гг на обьект или за обьект
                    if sprite.rect.centery > player.rect.centery:
                        # если Yцентр спрайта выше гг отрисовывать его перед гг
                        sprite.z = LAYERS['forward_' +
                                          list(LAYERS.keys())[sprite.z].split('_')[1]]
                    else:
                        # наоборот рисовать сзади гг
                        sprite.z = LAYERS['back_' +
                                          list(LAYERS.keys())[sprite.z].split('_')[1]]
                if sprite.z == layer:
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    self.display_surf.blit(sprite.image, offset_rect)
