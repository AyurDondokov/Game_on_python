"""Модуль с полезными функциями"""
import pygame
from os import walk
from csv import reader
from properties import TILE_SIZE


def import_folder(path: str) -> list:
    """Функция, которая читает все изображения в директории и создает из них surface'ы"""
    surface_list = []
    for _, _, img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            image_surface = pygame.image.load(full_path).convert_alpha()
            if path=='levels_data/graphics/decoration/clouds':
                image_surface.set_alpha(50)
            surface_list.append(image_surface)
    return surface_list


def import_csv_layout(path):
    """Функция, которая преобразовывает csv файл слоя в массив с id каждого тайла слоя"""
    terrain_map = []
    with open(path) as map:
        level = reader(map, delimiter=',')
        for row in level:
            terrain_map.append(list(row))
        return terrain_map

def import_cut_graphics(path):
    """Функция, которая 'режет' исходную png на тайловые surface"""
    surface = pygame.image.load(path).convert_alpha()
    tile_num_x = int(surface.get_size()[0] / TILE_SIZE)
    tile_num_y = int(surface.get_size()[1] / TILE_SIZE)

    cut_tiles = []
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * TILE_SIZE
            y = row * TILE_SIZE
            new_surf = pygame.Surface((TILE_SIZE,TILE_SIZE),flags = pygame.SRCALPHA)
            new_surf.blit(surface,(0,0),pygame.Rect(x,y,TILE_SIZE,TILE_SIZE))
            cut_tiles.append(new_surf)

    return cut_tiles
