"""Модуль, где описан класс для персонажей"""
import pygame
from properties import *
from support import *
from game_object import GameObject
import logging as log


class NPC(GameObject):
    def __init__(self, position: tuple, sprite_group: pygame.sprite.Group):
        super().__init__(position, sprite_group,
                         "./sprites/test_npc/", LAYERS['npc'], DEFAULT_CHARACTER_SPEED, True,
                         DEFAULT_CHARACTER_ANIM_SPEED, STANDARD_CHARACTER_ANIM_PACK)
        self.hitbox = self.rect.copy()

    def update(self, dt):
        self._animate(dt)
