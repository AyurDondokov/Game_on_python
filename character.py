"""Модуль, где описан класс для персонажей"""
import pygame
from dialog_system import Dialog
from properties import *
from support import *
from game_object import GameObject
from scripts import LocateCharacter
import logging as log


class InteractComponent():
    def __init__(self, group, pos: tuple, image_path: str, func) -> None:
        self.state = True
        self.func = func
        self._group = group
        self.is_able = False
        self._icon = GameObject(
            position=pos,
            sprite_group=self._group,
            sprite_path=image_path,
            z=LAYERS['ux']
        )

    def display_icon(self):
        """убирает иконку из группы спрайтов для отрисовки"""
        if self.state:
            if self.is_able:
                self._icon.add(self._group)
            else:
                self._icon.remove(self._group)

    def kill(self):
        """Делает компонент неактивным"""
        self._icon.kill()
        self.state = False

    def interact(self):
        self.func()


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
        self.name = name
        # Инициализация диалога
        if not dialog_replicas:
            dialog_replicas = {"1": ["???: ..."]}
        self.dialog_replicas = dialog_replicas
        self.dialog = Dialog(self.dialog_replicas["1"], self.notify_script)

        # чтобы взаимодействовать с обьектом
        # необходимо передать функцию при взаимодействии
        self.interact_component = InteractComponent(
            self.groups()[0],
            (self.rect.centerx, self.rect.centery - 100),
            "./sprites/dialog_icon.png",
            self.dialog.next_replica
        )

    def switch_replica(self, loc):
        self.dialog.replicas = self.dialog_replicas[loc]
        print(self.dialog_replicas)

    def notify_script(self, values: str):
        for command in values.split("|"):
            print(command)
            if command.startswith(" to_"):
                self.switch_replica(command.split(self.name)[1][2:])
            if command.startswith("locate"):
                self.locate(list(map(int, command[6:].split(","))))

    def update(self, dt):
        super().update(dt)
        self.interact_component.display_icon()

        if self.interact_component.is_able:
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

        self.interact_component = InteractComponent(
            self.groups()[0],
            (self.rect.topright[0], self.rect.topright[1] - 80),
            "./sprites/use_icon.png",
            self.execute
        )

        self._active = False
        dialog_replicas = ["Ната:Он разрушен", "Ната:Что же мне делать..."]
        self.dialog = Dialog(dialog_replicas)

    def activate(self):
        self._active = True

    def execute(self):
        if self._active:
            self.__set_current_level(self.move_to)
        else:
            self.dialog.next_replica()

    def update(self, dt):
        self.interact_component.display_icon()
        if self.interact_component.is_able and not self._active:
            self.dialog.update(dt)


class Component(GameObject):
    def __init__(self, position: tuple, sprite_group: pygame.sprite.Group, script):
        super().__init__(position,
                         sprite_group,
                         sprite_path="./levels_data/graphics/decoration/ruined_portal/destroy_portal_components.png",
                         z=LAYERS['ground'],
                         hitbox_offset=(0, 0.25),
                         )
        self.state = True
        self.__script = script
        self.hitbox = self.rect.copy().inflate(-self.rect.width * 0, -self.rect.height * 0)

        self.interact_component = InteractComponent(
            self.groups()[0],
            (self.rect.topright[0], self.rect.topright[1] - 80),
            "./sprites/use_icon.png",
            self.execute
        )

    def execute(self):
        self.state = False
        self.interact_component.kill()
        self.kill()

        self.__script.execute()

    def update(self, dt):
        self.interact_component.display_icon()
