import pygame
from support import import_csv_layout, import_cut_graphics
from properties import *
from tile import Tile, Trigger, Portal_components, Rocks
from player import Player
from decoration import Clouds
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

        # limiters
        limiters_layout = import_csv_layout(self.map['limiters'])
        self.limiters_sprites = self.create_tile_group(
            limiters_layout, 'limiters')

        # sky
        sky_layout = import_csv_layout(self.map['sky'])
        self.sky_sprites = self.create_tile_group(sky_layout, 'sky')

        # island ends
        island_ends_layout = import_csv_layout(self.map['island ends'])
        self.island_ends_sprites = self.create_tile_group(
            island_ends_layout, 'island ends')

        # grass
        grass_layout = import_csv_layout(self.map['grass'])
        self.grass_sprites = self.create_tile_group(grass_layout, 'grass')

        # grass elements
        grass_elements_layout = import_csv_layout(self.map['grass elements'])
        self.grass_elements_sprites = self.create_tile_group(
            grass_elements_layout, 'grass elements')

        # sand
        sand_layout = import_csv_layout(self.map['sand'])
        self.sand_sprites = self.create_tile_group(sand_layout, 'sand')

        # sand hole
        sand_hole_layout = import_csv_layout(self.map['sand hole'])
        self.sand_hole_sprites = self.create_tile_group(
            sand_hole_layout, 'sand hole')

        # crater
        crater_layout = import_csv_layout(self.map['crater'])
        self.crater_sprites = self.create_tile_group(crater_layout, 'crater')

        # portal components
        portal_components_layout = import_csv_layout(
            self.map['portal components'])
        self.portal_components_sprites = self.create_tile_group(
            portal_components_layout, 'portal components')

        # plants
        plants_layout = import_csv_layout(self.map['plants'])
        self.plants_sprites = self.create_tile_group(plants_layout, 'plants')

        # water
        water_layout = import_csv_layout(self.map['water'])
        self.water_sprites = self.create_tile_group(water_layout, 'water')

        # rocks
        rocks_layout = import_csv_layout(self.map['rocks'])
        self.rocks_sprites = self.create_tile_group(rocks_layout, 'rocks')

        # player(start point)
        player_layout = import_csv_layout(self.map['character'])
        self.player_setup(player_layout)

        # ruined portal
        ruined_portal_layout = import_csv_layout(self.map['ruined portal'])
        self.ruined_portal_sprites = self.create_tile_group(
            ruined_portal_layout, 'ruined portal')

        # flowers
        flowers_layout = import_csv_layout(self.map['flowers'])
        self.flowers_sprites = self.create_tile_group(
            flowers_layout, 'flowers')

        # decoration
        level_width = len(island_ends_layout[0]) * TILE_SIZE
        self.clouds = Clouds(SCREEN_HEIGHT*2, level_width,
                             30, self.all_sprites)

    def create_tile_group(self, layout, type):
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                # если не пустая клетка
                if val != '-1':
                    x = col_index * TILE_SIZE
                    y = row_index * TILE_SIZE

                    if type == 'grass':
                        grass_tile_list = import_cut_graphics(
                            'levels_data/graphics/decoration/grass/hub_grass.png')
                        tile_surface = grass_tile_list[int(val)]
                        Tile((x, y), self.all_sprites, tile_surface)

                    if type == 'grass elements':
                        grass_elements_tile_list = import_cut_graphics(
                            'levels_data/graphics/decoration/grass/hub_grass_elements.png')
                        tile_surface = grass_elements_tile_list[int(val)]
                        Tile((x, y), self.all_sprites, tile_surface)

                    if type == 'sky':
                        sky_tile_list = import_cut_graphics(
                            'levels_data/graphics/decoration/sky/sky.png')
                        tile_surface = sky_tile_list[int(val)]
                        Tile((x, y), self.all_sprites, tile_surface)

                    if type == 'water':
                        water_tile_list = import_cut_graphics(
                            'levels_data/graphics/decoration/water/hub_water.png')
                        tile_surface = water_tile_list[int(val)]
                        Tile((x, y), self.all_sprites, tile_surface)

                    if type == 'sand':
                        sand_tile_list = import_cut_graphics(
                            'levels_data/graphics/decoration/sand/hub_sand.png')
                        tile_surface = sand_tile_list[int(val)]
                        Tile((x, y), self.all_sprites, tile_surface)

                    if type == 'sand hole':
                        sand_hole_tile_list = import_cut_graphics(
                            'levels_data/graphics/decoration/sand/water_hole.png')
                        tile_surface = sand_hole_tile_list[int(val)]
                        Tile((x, y), self.all_sprites, tile_surface)

                    if type == 'flowers':
                        flowers_tile_list = import_cut_graphics(
                            'levels_data/graphics/decoration/flowers/chamomiles.png')
                        tile_surface = flowers_tile_list[int(val)]
                        Tile((x, y), self.all_sprites, tile_surface)

                    if type == 'ruined portal':
                        ruined_portal_tile_list = import_cut_graphics(
                            'levels_data/graphics/decoration/ruined_portal/big_destroy_portal.png')
                        tile_surface = ruined_portal_tile_list[int(val)]
                        Tile((x, y), self.all_sprites, tile_surface)

                    if type == 'portal components':
                        Portal_components((x, y), self.all_sprites)

                    if type == 'rocks':
                        if val == '0':
                            sprite = Rocks((x, y), self.all_sprites, pygame.image.load(
                                'levels_data/graphics/decoration/rocks/rock1.png').convert_alpha())
                        if val == '1':
                            sprite = Rocks((x, y), self.all_sprites, pygame.image.load(
                                'levels_data/graphics/decoration/rocks/rock2.png').convert_alpha())

                    if type == 'crater':
                        crater_tile_list = import_cut_graphics(
                            'levels_data/graphics/decoration/crater/hub_crater.png')
                        tile_surface = crater_tile_list[int(val)]
                        Tile((x, y), self.all_sprites, tile_surface)

                    if type == 'plants':
                        plants_tile_list = import_cut_graphics(
                            'levels_data/graphics/decoration/plants/plant.png')
                        tile_surface = plants_tile_list[int(val)]
                        Tile((x, y), self.all_sprites, tile_surface)

                    if type == 'island ends':
                        island_ends_tile_list = import_cut_graphics(
                            'levels_data/graphics/decoration/ends_of_island/ends_of_island.png')
                        tile_surface = island_ends_tile_list[int(val)]
                        Tile((x, y), self.all_sprites, tile_surface)

                    if type == 'limiters':
                        limiters_tile_list = import_cut_graphics(
                            'levels_data/graphics/decoration/limiters/limiters.png')
                        tile_surface = limiters_tile_list[int(val)]
                        Tile((x, y), [self.all_sprites,
                             self.collision_sprites], tile_surface)

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
