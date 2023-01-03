"""Модуль, где описан класс для персонажей"""
import pygame
from dialog_system import Dialog
from properties import *
from support import *
from game_object import GameObject
import logging as log


"""
{a:[{},{}]} так не надо

1,"ключ"

{a:
    {
        "1":["45","56],
        "2":["87","16],
        "Babla":["87","16],
        "Еще Babla":["87","16],
    
    
    }
}

"""


class NPC(GameObject):
    def __init__(self, position: tuple, sprite_group: pygame.sprite.Group, name: str, dialog_replicas: tuple = None):
        super().__init__(position,
                         sprite_group,
                         sprite_path=f"./sprites/npc/{name}/",
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

        self.dialog = Dialog(self.dialog_replicas[0]["1"])
        print()
        print(dialog_replicas)
        self.is_dialog_able = False
        self.dialog_icon = GameObject(
            position=(self.rect.centerx, self.rect.centery - 100),
            sprite_group=self.groups()[0],
            sprite_path='./sprites/dialog_icon.png',
            z=LAYERS['ux']
        )
        self.display_dialog_icon()

    def switch_dialog(self, loc):
        self.dialog_replicas = self.dialog_replicas[int(loc)-1][loc]
        print(self.dialog_replicas)

    def display_dialog_icon(self):
        """убирает иконку из группы спрайтов для отрисовки"""
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
    def __init__(self, position: tuple, sprite_group: pygame.sprite.Group, set_current_level, move_to):
        super().__init__(position,
                         sprite_group,
                         sprite_path="./images/ground/trigger.png",
                         z=LAYERS['ground'],
                         hitbox_offset=(0, 0.25),
                         movement_speed=DEFAULT_CHARACTER_SPEED,
                         is_animated=False,
                         anim_speed=DEFAULT_CHARACTER_ANIM_SPEED,
                         animations_pack=STANDARD_CHARACTER_ANIM_PACK
                         )
        self.__set_current_level = set_current_level
        self.move_to = move_to
        self.hitbox = self.rect.copy().inflate(-self.rect.width * 0, -self.rect.height * 0)
        self.is_use_able = False
        self.__use_icon = GameObject(
            position=(self.rect.topright[0], self.rect.topright[1] - 80),
            sprite_group=self.groups()[0],
            sprite_path='./sprites/use_icon.png',
            z=LAYERS['ux']
        )

    def display_dialog_icon(self):
        if self.is_use_able:
            self.__use_icon.add(self.groups()[0])
        else:
            self.__use_icon.remove(self.groups()[0])

    def execute(self):
        self.__set_current_level(self.move_to)

    def update(self, dt):
        # super().update(dt)
        self.display_dialog_icon()
