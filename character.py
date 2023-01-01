"""Модуль, где описан класс для персонажей"""
import pygame
from dialog_system import Dialog
from properties import *
from support import *
from game_object import GameObject
import logging as log


class NPC(GameObject):
    def __init__(self, position: tuple, sprite_group: pygame.sprite.Group, name,
                 dialog_replicas: tuple = None):
        super().__init__(position,
                         sprite_group,
                         sprite_path="./sprites/test_npc/",
                         z=LAYERS['forward_npc'],
                         hitbox_offset=(0, 0.25),
                         movement_speed=DEFAULT_CHARACTER_SPEED,
                         is_animated=True,
                         anim_speed=DEFAULT_CHARACTER_ANIM_SPEED,
                         animations_pack=STANDARD_CHARACTER_ANIM_PACK
                         )
        self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.2, -self.rect.height * 0.5)

        # Инициализация диалога
        self.dialog_replicas = dialog_replicas
        self.dialog = Dialog(dialog_replicas)
        self.is_dialog_able = False
        self.dialog_icon = GameObject(
            position=(self.rect.centerx, self.rect.centery - 100),
            sprite_group=self.groups()[0],
            sprite_path='./sprites/dialog_icon.png',
            z=LAYERS['ux']
        )
        self.display_dialog_icon()

    def display_dialog_icon(self):
        if self.dialog_replicas and self.is_dialog_able:
            self.dialog_icon.add(self.groups()[0])
        else:
            self.dialog_icon.remove(self.groups()[0])

    def update(self, dt):
        super().update(dt)
        self.display_dialog_icon()

        if self.is_dialog_able:
            self.dialog.update(dt)


class Portal(GameObject):
    def __init__(self, position: tuple, sprite_group: pygame.sprite.Group):
        print("Portal initialized")
        super().__init__(position,
                         sprite_group,
                         sprite_path="./levels_data/graphics/decoration/ruined_portal/big_destroy_portal.png",
                         z=LAYERS['forward_npc'],
                         hitbox_offset=(0, 0.25),
                         movement_speed=DEFAULT_CHARACTER_SPEED,
                         is_animated=False,
                         anim_speed=DEFAULT_CHARACTER_ANIM_SPEED,
                         animations_pack=STANDARD_CHARACTER_ANIM_PACK
                         )
        self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.2, -self.rect.height * 0.5)
        self.is_use_able = False
        self.use_icon = GameObject(
            position=(self.rect.topright[0] + 40, self.rect.topright[1] - 80),
            sprite_group=self.groups()[0],
            sprite_path='./sprites/use_icon.png',
            z=LAYERS['ux']
        )

    def display_dialog_icon(self):
        if self.is_use_able:
            self.use_icon.add(self.groups()[0])
        else:
            self.use_icon.remove(self.groups()[0])

    def update(self, dt):
        super().update(dt)
        self.display_dialog_icon()
