"""Модуль, где описан класс игрока"""
import pygame
from properties import *
from support import *
from game_object import GameObject


class Player(GameObject):
    def __init__(self, position: tuple, sprite_group: pygame.sprite.Group):
        super().__init__(position, sprite_group,
                         "./sprites/main_character/", LAYERS['player'], DEFAULT_CHARACTER_SPEED, True,
                         DEFAULT_CHARACTER_ANIM_SPEED, STANDARD_CHARACTER_ANIM_PACK)

    def _input(self):
        """Приём нажатия клавишь"""
        keys = pygame.key.get_pressed()

        # Вертикальное движение
        if keys[pygame.K_w] and not keys[pygame.K_s]:
            self.direction.y = -1
        elif keys[pygame.K_s] and not keys[pygame.K_w]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        # Горизонтальное движение
        if keys[pygame.K_a] and not keys[pygame.K_d]:
            self.direction.x = -1
        elif keys[pygame.K_d] and not keys[pygame.K_a]:
            self.direction.x = 1
        else:
            self.direction.x = 0
