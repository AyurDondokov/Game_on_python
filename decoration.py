from properties import *
import pygame
from tile import Tile
from support import import_folder
from random import choice, randint

class Clouds:
    def __init__(self, horizon, level_width, cloud_number, group):
        cloud_surf_list = import_folder('levels_data/graphics/decoration/clouds')
        min_x = -SCREEN_WIDTH
        max_x = level_width + SCREEN_WIDTH
        min_y = 0
        max_y = horizon
        self.cloud_sprites = pygame.sprite.Group()

        for cloud in range(cloud_number):
            cloud = choice(cloud_surf_list)
            x = randint(min_x, max_x)
            y = randint(min_y, max_y)
            Tile((x, y), group, cloud) 
