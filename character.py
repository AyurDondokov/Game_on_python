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
    def __init__(self, position: tuple, sprite_group: pygame.sprite.Group, name: str):
        super().__init__(position,
                         sprite_group,
                         sprite_path="./sprites/test_npc/",
                         z=LAYERS['npc'],
                         hitbox_offset=(0, 0.25),
                         movement_speed=DEFAULT_CHARACTER_SPEED,
                         is_animated=True,
                         anim_speed=DEFAULT_CHARACTER_ANIM_SPEED,
                         animations_pack=STANDARD_CHARACTER_ANIM_PACK
                         )
        self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.2, -self.rect.height * 0.5)
        self.name = name

        self.is_dialog_able = False
        self.dialog_icon = GameObject(
            position=(self.rect.centerx + 40, self.rect.centery - 80),
            sprite_group=self.groups()[0],
            sprite_path='./sprites/dialog_icon.png',
            z=self.z
        )
        self.display_dialog_icon()

    def make_dialog(self):
        print(f"dialog with {self.name}")
        pass

    def display_dialog_icon(self):
        if self.is_dialog_able:
            self.dialog_icon.add(self.groups()[0])
        else:
            self.dialog_icon.remove(self.groups()[0])

    def _input(self):
        """Приём нажатия клавишь"""
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            if self.is_dialog_able:
                self.make_dialog()

    def update(self, dt):
        super().update(dt)
        self.display_dialog_icon()
