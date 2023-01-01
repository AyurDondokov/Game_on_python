import logging
import sys

import pygame

from character import NPC, Portal
from decoration import Clouds
from player import Player
from properties import *
from replicas_data import test_npc, test_npc2
from support import import_csv_layout, import_cut_graphics
from tile import Tile, Trigger, NotTiledImage
from pytmx.util_pygame import load_pygame
from scripts import TestScript


log = logging.getLogger(__name__)


class Level:
    def __init__(self, level_data, current_level):
        """Отрисовка спрайтов на уровне"""

        log.info(f'Level class intialization')
        self.display_surface = pygame.display.get_surface()

        # для перемещения между уровнями
        self.cur_lvl = current_level
        self.lvl_to = level_data["move_to"]
        self.map = level_data["MAP"]
        self.tileset = level_data["TileSet"]
        self.tmx_data = load_pygame(level_data["TMXData"])

        self.all_sprites = CameraGroup()
        self.collision_sprites = pygame.sprite.Group()
        self.interactable_sprites = pygame.sprite.Group()
        self.trigger_sprites = pygame.sprite.Group()

        self.create_map()
        self.setup()

    def setup(self):
        """Загрузка важных объектов на уровне"""
        self.test_npc = NPC(
            position=(900, 450),
            sprite_group=[self.all_sprites,
                          self.collision_sprites, self.interactable_sprites],
            name='Ayur',
            dialog_replicas=test_npc)
        self.test_npc2 = NPC(
            position=(1320, 450),
            sprite_group=[self.all_sprites,
                          self.collision_sprites, self.interactable_sprites],
            name='Ayur',
            dialog_replicas=test_npc2)
        # Триггер для начала боя
        # В будущем должен создаваться с помощью csv
        Trigger((1200, 500), [self.all_sprites, self.trigger_sprites],
                pygame.image.load("images/ground/trigger.png"), TestScript(None))

        # загрузка обьектов из tmx файла
        for layer in self.tmx_data.layernames.values():
            for obj in layer:
                groups = [self.all_sprites]
                if obj.properties.get("collide"):
                    # если объекту было назначаенно свойство в Tiled, то..
                    groups.append(self.collision_sprites)
                Tile((obj.x, obj.y), groups,  obj.image, LAYERS["ground"])

    def create_map(self):
        for key in self.map:
            if key != "character":
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

                    if (type == 'limiters'):
                        Tile((x, y), [self.all_sprites,
                                      self.collision_sprites], import_cut_graphics(self.tileset[type])[int(val)])
                    else:
                        Tile((x, y), self.all_sprites, import_cut_graphics(self.tileset[type])[int(val)])

    def player_setup(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val == '0':
                    x = col_index * TILE_SIZE
                    y = row_index * TILE_SIZE
                    self.player = Player((x, y), self.all_sprites,
                                         self.collision_sprites, self.interactable_sprites, self.trigger_sprites)

    def run(self, dt):
        """Запусе отрисовки уровня"""
        self.events_list = pygame.event.get()

        # список событий передаётся компонентам для самостоятельной обработки
        self.player.set_events_list(self.events_list)
        # выход из игры
        for event in self.events_list:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.pause_def()
                if event.key == pygame.K_1:
                    self.cur_lvl(self.lvl_to)

        self.all_sprites.custom_draw(self.player)
        self.all_sprites.update(dt)

    def pause_def(self):

        # TODO: сделать так чтобы при одновременном нажатии esc и удержании кнопки перемещения,
        # перемещение не происходило

        self.pause_menu = True
        # цикл замараживает всю остальную часть кода
        while self.pause_menu:
            log.debug(f"pause active")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.pause_menu = False
            self.all_sprites.custom_draw(self.player)
            self.window = pygame.sprite.Sprite()
            self.window.image = pygame.image.load('./sprites/pause_menu.png')
            self.window.rect = self.window.image.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
            self.display_surface.blit(self.window.image, self.window.rect)
            pygame.display.update()


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
