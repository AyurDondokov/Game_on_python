import pygame
from support import import_csv_layout, import_cut_graphics
from properties import *
from tile import Tile, Trigger, NotTiledImage
from player import Player
from decoration import Clouds
import logging
from character import NPC
import sys

log = logging.getLogger(__name__)
"""Отрисовка спрайтов на уровне"""


class Level:
    def __init__(self, level_map, level_tileset, current_level, lvl_go_to):
        log.info(f'Level class intialization')
        self.display_surface = pygame.display.get_surface()

        # для перемещения между уровнями
        self.cur_lvl = current_level
        self.lvl_to = lvl_go_to

        self.map = level_map
        self.tileset = level_tileset
        self.all_sprites = CameraGroup()
        self.collision_sprites = pygame.sprite.Group()
        self.interactable_sprites = pygame.sprite.Group()
        self.create_map()
        self.setup()

    def setup(self):
        """Загрузка важных объектов на уровне"""
        self.test_npc = NPC(
            position=(700, 600),
            sprite_group=[self.all_sprites,
                          self.collision_sprites, self.interactable_sprites],
            name='Ayur',
            dialog_replicas=('Ayur:Hello', 'Ayur:My name is Ayur', 'Ayur:Its first dialog in game'))

    def create_map(self):
        for key in self.map:
            if key!="character":
                self.create_tile_group(import_csv_layout(self.map[key]), key)
            else:
                self.player_setup(import_csv_layout(self.map[key]))

        # decoration
        level_width = len(import_csv_layout(self.map['island ends'])[0]) * TILE_SIZE
        self.clouds = Clouds(SCREEN_HEIGHT*2, level_width,
                             30, self.all_sprites)

    def create_tile_group(self, layout, type):
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                # если не пустая клетка
                if val != '-1':
                    x = col_index * TILE_SIZE
                    y = row_index * TILE_SIZE

                    
                    if type == 'portal components':
                        NotTiledImage((x, y), self.all_sprites,  pygame.image.load(self.tileset[type]).convert_alpha())
                    elif type == 'rocks':
                        if val == '0':
                            NotTiledImage((x, y), self.all_sprites,  pygame.image.load(self.tileset[type][0]).convert_alpha())
                        if val == '1':
                            NotTiledImage((x, y), self.all_sprites,  pygame.image.load(self.tileset[type][1]).convert_alpha())
                    elif (type == 'ruined portal') or (type == 'limiters'):
                        Tile((x, y), [self.all_sprites,
                            self.collision_sprites], import_cut_graphics(self.tileset[type])[int(val)])
                    else:
                        Tile((x, y), self.all_sprites, import_cut_graphics(self.tileset[type])[int(val)])

    def player_setup(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                if val == '0':
                    self.player = Player((x, y), self.all_sprites,
                                         self.collision_sprites, self.interactable_sprites)

    def run(self, dt):
        self.events_list = pygame.event.get()
        # список событий передаётся компонентам для самостоятельной обработки
        self.player.set_events_list(self.events_list)
        for event in self.events_list:
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
