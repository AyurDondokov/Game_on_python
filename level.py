import scripts as scr
from scripts import *
import logging
import sys

import pygame

from reader_dialog import ReadingLocations
import battle_system
import UI
import battle_system
import game_object
from scripts import ActivatePortalScript
from character import Portal, Component
from character import NPC
from player import Player
from properties import *
from replicas_data import test_npc2
from support import import_csv_layout, import_cut_graphics
from tile import Tile, Trigger
from pytmx.util_pygame import load_pygame


log = logging.getLogger(__name__)


class Level:
    def __init__(self, level_data, set_current_level, name):
        """Отрисовка спрайтов на уровне"""
        self.is_paused = None
        self.player = None
        self.window = None
        self.events_list = None
        log.info(f'Level class intialization')
        self.name = name
        self.reader = ReadingLocations(f'dialog/{self.name}.txt')

        self.is_runned = False
        self.__display_surface = pygame.display.get_surface()

        # для перемещения между уровнями
        self.set_current_level = set_current_level
        self.move_to = level_data["move_to"]

        pygame.mixer.music.load("music_and_sound/music/menu/mmF.mp3")
        pygame.mixer.music.play(-1)

        # Меню паузы
        # buttons = (
        #     UI.Button(self.pause, None, (SCREEN_WIDTH/2, SCREEN_HEIGHT*0.2),
        #               image_path="./sprites/pause_menu/button.png",
        #               selected_image_path="./sprites/pause_menu/button_hover.png",
        #               sprite_group=self.__all_sprites,
        #               text="Продолжить",
        #
        #               ),
        # )
        # self.pause_menu = UI.Menu(buttons,
        #                           action_bar_path="./sprites/pause_menu/menu_background.png")


        # отрисовка
        self.__map = level_data["MAP"]
        self.__tileset = level_data["TileSet"]
        self.__tmx_data = load_pygame(level_data["TMXData"])

        self.battles_data = level_data["battles"]

        self.__music_path = level_data["music"]

        self.__all_sprites = CameraGroup()
        self.__collision_sprites = pygame.sprite.Group()
        self.__interactable_sprites = pygame.sprite.Group()
        self.__trigger_sprites = pygame.sprite.Group()
        self.__npc_dict = {}
        # Меню паузы
        buttons = (
            UI.Button(self.pause, None, (SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.2),
                      image_path="./sprites/pause_menu/button.png",
                      selected_image_path="./sprites/pause_menu/button_hover.png",
                      sprite_group=[],
                      text="Продолжить",
                      text_color=GRAY,
                      selected_text_color=WHITE,
                  ),
            UI.Button(self.save, None, (SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.4),
                      image_path="./sprites/pause_menu/button.png",
                      selected_image_path="./sprites/pause_menu/button_hover.png",
                      sprite_group=[],
                      selected_text_color=WHITE,
                      text="Сохранить",
                      text_color=GRAY
                      ),
            UI.Button(self.load, None, (SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.6),
                      image_path="./sprites/pause_menu/button.png",
                      selected_image_path="./sprites/pause_menu/button_hover.png",
                      sprite_group=[],
                      text="Загрузить",
                      text_color=GRAY,
                      selected_text_color=WHITE
                      ),
            UI.Button(self.exit, None, (SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.8),
                      image_path="./sprites/pause_menu/button.png",
                      selected_image_path="./sprites/pause_menu/button_hover.png",
                      sprite_group=[],
                      text="Выйти",
                      text_color=GRAY,
                      selected_text_color=WHITE
                      ),
        )
        self.pause_menu = UI.Menu(buttons,
                                  action_bar_path="./sprites/pause_menu/menu_background.png",
                                  pos=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))

        self.__create_map()
        self.__setup()

    def __setup(self):
        """Загрузка важных объектов на уровне"""
        self.battle_manager = battle_system.BattleManager(self.battles_data, self.player, self.__music_path)

        # загрузка обьектов из tmx файла
        for layer in self.__tmx_data.layernames.values():
            print('layer', layer)
            for obj in layer:
                print('obj', obj)
                # если объекту было назначаенно свойство в Tiled, то..
                groups = [self.__all_sprites]
                if obj.properties.get("collide"):
                    groups.append(self.__collision_sprites)
                if obj.name == "Portal":
                    obj_image = obj.image.get_rect()
                    # невидимый для игрока объект с которым он будет взаимодейтсвовать как с порталом
                    pos = (obj.x+obj_image.centerx - TILE_SIZE / 2, obj.y+obj_image.bottom - TILE_SIZE)
                    portal = Portal(pos,
                                    [self.__all_sprites, self.__interactable_sprites],
                                    self.set_current_level,
                                    self.move_to)
                    # отображение портала
                    Tile((obj.x, obj.y), groups, obj.image, LAYERS["back_decor"])
                if obj.name == "component":
                    script = ActivatePortalScript(None)
                    Component((obj.x, obj.y), [self.__all_sprites, self.__interactable_sprites], script)

                elif hasattr(obj, "class"):
                    if getattr(obj, "class") == "battle":
                        Trigger(
                            pos=(obj.x, obj.y),
                            groups=[self.__all_sprites, self.__trigger_sprites],
                            surface=pygame.image.load("images/ground/trigger.png"),
                            script=scr.StartBattleScript(self.battle_manager, obj.properties.get("battle_index"))
                        )
                        print(obj.x, obj.y)
                    if getattr(obj, "class") == "npc":
                        dialog = None
                        if obj.properties.get("dialog"):
                            dialog = self.reader.get_npc_replicas(obj.name)
                        self.__npc_dict.update(
                            {obj.name:
                             NPC((obj.x, obj.y),
                                 [self.__all_sprites, self.__collision_sprites, self.__interactable_sprites],
                                 obj.name, dialog_replicas=dialog)}
                        )
                else:
                    if hasattr(obj, "hitbox_offset_x"):
                        game_object.GameObject((obj.x, obj.y), groups, "", LAYERS["back_decor"],
                                               image_surf=obj.image,
                                               hitbox_offset=(getattr(obj, "hitbox_offset_x"), getattr(obj, "hitbox_offset_y")),
                                               hitbox_size=(getattr(obj, "hitbox_size_x"), getattr(obj, "hitbox_size_y")))
                    else:
                        game_object.GameObject((obj.x, obj.y), groups, "", LAYERS["back_decor"],
                                               image_surf=obj.image)
        script.receiver = portal

    def __create_map(self):
        print("self.__map", self.__map)
        for key in self.__map:

            if key != "character":
                print("key", self.__map[key], key)
                self.__create_tile_group(import_csv_layout(self.__map[key]), key)
            else:
                self.__player_setup(import_csv_layout(self.__map[key]))

        # TODO: сделать совместимым с разными картами:
        # decoration
        # level_width = len(import_csv_layout(self.map['island ends'])[0]) * TILE_SIZE
        # self.clouds = Clouds(SCREEN_HEIGHT*2, level_width,
        #                      30, self.all_sprites)

    def __create_tile_group(self, layout, tile_type):
        cut_tileset = import_cut_graphics(self.__tileset[tile_type])
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                # если не пустая клетка
                if val != '-1':
                    x = col_index * TILE_SIZE
                    y = row_index * TILE_SIZE

                    if tile_type == 'limiters':
                        Tile((x, y), [self.__all_sprites,
                                      self.__collision_sprites], cut_tileset[int(val)])
                    else:
                        Tile((x, y), self.__all_sprites, cut_tileset[int(val)])

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
        for event in self.events_list:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.pause()
                if event.key == pygame.K_1:
                    self.set_current_level(self.move_to)

        # список событий передаётся компонентам для самостоятельной обработки
        if not self.is_paused:
            self.player.set_events_list(self.events_list)

            if not self.battle_manager.is_battle:
                self.__all_sprites.centralize_on_obj(self.player)
                self.__all_sprites.custom_draw(self.player)
                self.__all_sprites.update(dt)
            else:
                self.battle_manager.update(dt)
                self.battle_manager.set_events_list(self.events_list)
        else:
            self.__all_sprites.custom_draw(self.player)
            self.pause_menu.set_events_list(self.events_list)
            self.pause_menu.draw_menu()
            self.pause_menu.input()
            self.pause_menu.update()

        pygame.display.update()

    def pause(self):
        self.is_paused = not self.is_paused
        print(self.is_paused)

    def save(self):
        pass

    def load(self):
        pass

    def settings(self):
        pass

    def exit(self):
        pass


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
                if abs(player.rect.x - sprite.rect.x) <= SCREEN_WIDTH*0.75 and \
                        abs(player.rect.y - sprite.rect.y) <= SCREEN_HEIGHT*0.75:
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
