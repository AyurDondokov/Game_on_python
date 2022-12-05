"""Модуль с полезными функциями"""
import pygame
from os import walk


def import_folder(path: str) -> list:
    """Функция, которая читает все изображения в директории и создает из них surface'ы"""
    surface_list = []
    for _, _, img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            image_surface = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surface)
    # print(surface_list)
    return surface_list
