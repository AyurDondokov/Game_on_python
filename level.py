import logging
import sys

import pygame

from character import NPC, Portal
from battle_system import Battle
from character import NPC
from decoration import Clouds
from player import Player
from properties import *
from replicas_data import test_npc, test_npc2
from support import import_csv_layout, import_cut_graphics
from tile import Tile, Trigger, NotTiledImage
from pytmx.util_pygame import load_pygame
from scripts import TestScript

import scripts as scr

log = logging.getLogger(__name__)


class Level:
    def __init__(self, level_data, set_current_level):
        """Отрисовка спрайтов на уровне"""
        self.events_list = None
        log.info(f'Level class intialization')

        self.is_runned = False
        self.__display_surface = pygame.display.get_surface()
        # для перемещения между уровнями
        self.set_current_level = set_current_level
        self.move_to = level_data["move_to"]
        # отрисовка
        self.__map = level_data["MAP"]
        self.__tileset = level_data["TileSet"]
        self.__tmx_data = load_pygame(level_data["TMXData"])

        self.__music_path = level_data["music"]

        self.__all_sprites = CameraGroup()
        self.__collision_sprites = pygame.sprite.Group()
        self.__interactable_sprites = pygame.sprite.Group()
        self.__trigger_sprites = pygame.sprite.Group()

        self.__create_map()
        self.__setup()

    def __setup(self):
        """Загрузка важных объектов на уровне"""
        self.test_battle = Battle(self.player, [TUMBLEWEED_ENEMY, TEST_ENEMY_2], self.__music_path)

        # Триггер для начала боя
        # В будущем должен создаваться с помощью csv
        Trigger((1200, 500), [self.__all_sprites, self.__trigger_sprites],
                pygame.image.load("images/ground/trigger.png"), scr.StartBattleScript(self.test_battle))

        # загрузка обьектов из tmx файла
        for layer in self.__tmx_data.layernames.values():
            for obj in layer:
                # если объекту было назначаенно свойство в Tiled, то..
                groups = [self.__all_sprites]
                if obj.properties.get("collide"):
                    groups.append(self.__collision_sprites)
                if obj.name == "Portal":
                    obj_image = obj.image.get_rect()
                    # невидимый для игрока объект с которым он будет взаимодейтсвовать как с порталом
                    pos = (obj.x+obj_image.centerx - TILE_SIZE / 2, obj.y+obj_image.bottom - TILE_SIZE)
                    Portal(pos,
                           [self.__all_sprites, self.__interactable_sprites],
                           self.set_current_level,
                           self.move_to)
                    # отображение портала
                    Tile((obj.x, obj.y), groups, obj.image, LAYERS["back_decor"])

                elif hasattr(obj, "class"):
                    if getattr(obj, "class") == "npc":
                        NPC((obj.x, obj.y),
                            [self.__all_sprites, self.__collision_sprites, self.__interactable_sprites],
                            obj.name, dialog_replicas=test_npc2)
                        pass
                else:
                    Tile((obj.x, obj.y), groups, obj.image, LAYERS["ground"])

    def __create_map(self):
        for key in self.__map:
            if key != "character":
                self.__create_tile_group(import_csv_layout(self.__map[key]), key)
            else:
                self.__player_setup(import_csv_layout(self.__map[key]))

        # TODO: сделать совместимым с разными картами:
        # decoration
        # level_width = len(import_csv_layout(self.map['island ends'])[0]) * TILE_SIZE
        # self.clouds = Clouds(SCREEN_HEIGHT*2, level_width,
        #                      30, self.all_sprites)

    def __create_tile_group(self, layout, type):
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                # если не пустая клетка
                if val != '-1':
                    x = col_index * TILE_SIZE
                    y = row_index * TILE_SIZE

                    if type == 'limiters':
                        Tile((x, y), [self.__all_sprites,
                                      self.__collision_sprites], import_cut_graphics(self.__tileset[type])[int(val)])
                    else:
                        Tile((x, y), self.__all_sprites, import_cut_graphics(self.__tileset[type])[int(val)])

    def __player_setup(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val == '0':
                    self.__player_x = col_index * TILE_SIZE
                    self.__player_y = row_index * TILE_SIZE
                    self.player = Player((self.__player_x, self.__player_y), self.__all_sprites,
                                         self.__collision_sprites, self.__interactable_sprites, self.__trigger_sprites)

    def start(self):
        pygame.mixer.music.load(self.__music_path)
        pygame.mixer.music.play(-1)
        self.is_runned = True
        self.player = Player((self.__player_x, self.__player_y), self.__all_sprites,
                             self.__collision_sprites, self.__interactable_sprites, self.__trigger_sprites)

    def run(self, dt):
        """Запусе отрисовки уровня"""
        if not self.is_runned:
            self.start()

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
                    self.set_current_level(self.move_to)

        if not self.test_battle.is_battle:
            self.__all_sprites.centralize_on_obj(self.player)
            self.__all_sprites.custom_draw(self.player)
            self.__all_sprites.update(dt)
        else:
            self.test_battle.update(dt)
            self.test_battle.set_events_list(self.events_list)
            self.test_battle.draw()

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
            self.__all_sprites.custom_draw(self.player)
            self.window = pygame.sprite.Sprite()
            self.window.image = pygame.image.load('./sprites/pause_menu.png')
            self.window.rect = self.window.image.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
            self.__display_surface.blit(self.window.image, self.window.rect)
            pygame.display.update()


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

        self.display_surf = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

    def centralize_on_obj(self, obj):
        self.offset.x = obj.rect.centerx - SCREEN_WIDTH / 2
        self.offset.y = obj.rect.centery - SCREEN_HEIGHT / 2

    def custom_draw(self, player):
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
