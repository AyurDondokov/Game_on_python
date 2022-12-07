"""Модуль, где описан класс для персонажей"""
import pygame
from properties import *
from support import *
from game_object import GameObject
import logging as log


class Dialog(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

        self.display_surf = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()


class NPC(GameObject):
    def __init__(self, position: tuple, sprite_group: pygame.sprite.Group, hitbox, name):
        super().__init__(position, sprite_group,
                         "./sprites/test_npc/", LAYERS['npc'], DEFAULT_CHARACTER_SPEED, True,
                         DEFAULT_CHARACTER_ANIM_SPEED, STANDARD_CHARACTER_ANIM_PACK)
        self.hitbox = self.rect.copy()
        self.name = name

    def make_dialog(self):
        pass

    def _input(self):
        """Приём нажатия клавишь"""
        keys = pygame.key.get_pressed()
        events = pygame.event.get()

        if keys[pygame.K_SPACE]:
            self.make_dialog()
