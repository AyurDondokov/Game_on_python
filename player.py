"""Модуль, где описан класс игрока"""
import pygame
from properties import *
from support import *
from game_object import GameObject
import logging as log
from tile import Trigger


class Player(GameObject):
    def __new__(cls, *args, **kwargs):
        """Реализация синглтона"""
        if not hasattr(cls, 'instance'):
            cls.instance = super(Player, cls).__new__(cls)
        return cls.instance

    def __init__(self, position: tuple[float, float],
                 sprite_group: pygame.sprite.Group,
                 collision_sprites: pygame.sprite.Group,
                 interactable_sprites: pygame.sprite.Group,
                 trigger_sprites: pygame.sprite.Group,
                 player_level: int = 1,
                 health: int = LEVELS_PROPERTIES[1]["max_health"],
                 exp: int = 0):
        super().__init__(position=position,
                         sprite_group=sprite_group,
                         sprite_path="./sprites/main_character/",
                         z=LAYERS['player'],
                         hitbox_offset=(0, 0.375),
                         hitbox_size=(0.8, 0.25),
                         movement_speed=DEFAULT_CHARACTER_SPEED,
                         is_animated=True,
                         anim_speed=DEFAULT_CHARACTER_ANIM_SPEED,
                         animations_pack=STANDARD_CHARACTER_ANIM_PACK)
        self.__collision_sprites = collision_sprites
        self.__interactable_sprites = interactable_sprites
        self.__trigger_sprites = trigger_sprites
        self.__event_list = []
        self.level = player_level
        self.health = health
        self._exp = exp

        self._managed = True

    def _collision(self, direction):
        """Проверка столкновений"""
        super(Player, self)._collision(direction)
        for sprite in self.__collision_sprites:
            if hasattr(sprite, 'hitbox'):
                if sprite.hitbox.colliderect(self.hitbox):

                    if direction == 'horizontal':
                        if self._direction.x > 0:
                            self.hitbox.right = sprite.hitbox.left
                        if self._direction.x < 0:
                            self.hitbox.left = sprite.hitbox.right

                        self.rect.centerx = self.hitbox.centerx - \
                            self.rect.width * self.hitbox_offset[0]
                        self._pos.x = self.hitbox.centerx - \
                            self.rect.width * self.hitbox_offset[0]

                    if direction == 'vertical':
                        if self._direction.y > 0:
                            self.hitbox.bottom = sprite.hitbox.top
                        if self._direction.y < 0:
                            self.hitbox.top = sprite.hitbox.bottom

                        self.rect.centery = self.hitbox.centery - \
                            self.rect.height * self.hitbox_offset[1]
                        self._pos.y = self.hitbox.centery - \
                            self.rect.height * self.hitbox_offset[1]
        # запуск триггеров
        for sprite in self.__trigger_sprites:
            if hasattr(sprite, 'hitbox'):
                if sprite.hitbox.colliderect(self.hitbox):
                    sprite.check()

    def _new_level(self):
        self.level += 1
        self.health = LEVELS_PROPERTIES[self.level]['max_health']

    def set_events_list(self, event_list):
        self.__event_list = event_list

    def _input(self, dt):
        """Приём нажатия клавишь"""
        if self._managed:
            keys = pygame.key.get_pressed()

            # Вертикальное движение
            if keys[pygame.K_w] and not keys[pygame.K_s]:
                self._direction.y = -1
                self._change_anim_status("walk_up")
            elif keys[pygame.K_s] and not keys[pygame.K_w]:
                self._direction.y = 1
                self._change_anim_status("walk_down")
            else:
                self._direction.y = 0

            # Горизонтальное движение
            if keys[pygame.K_a] and not keys[pygame.K_d]:
                self._direction.x = -1
                self._change_anim_status("walk_left")
            elif keys[pygame.K_d] and not keys[pygame.K_a]:
                self._direction.x = 1
                self._change_anim_status("walk_right")
            else:
                self._direction.x = 0

            if self._direction.magnitude() == 0:
                self._change_anim_status("idle_" + self._anim_status.split('_')[1])

        # чтение событий pygame.event
        keys = self.__event_list
        for event in keys:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    for sprite in self.__interactable_sprites:
                        # переключение на следующую реплику в диалоге
                        if hasattr(sprite, 'interact_component'):
                            if sprite.interact_component.is_able:
                                sprite.interact_component.interact()
                        # if hasattr(sprite, 'is_use_able'):
                        #     if sprite.is_use_able:
                        #         sprite.execute()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    print(self._pos)

    def check_npc_distance(self):
        """Если NPC близко отобразить иконку взаимодействия над NPC"""
        flag = False
        for sprite in self.__interactable_sprites:
            if hasattr(sprite, 'interact_component'):
                sprite.interact_component.is_able = self._pos.distance_to(
                    sprite.pos) < DISTANCE_FOR_INTERACT
                if hasattr(sprite, 'dialog'):
                    if sprite.dialog.is_open:
                        flag = True
                        self._managed = False
                        self._direction.x = 0
                        self._direction.y = 0
                        self._change_anim_status("idle_" + self._anim_status.split('_')[1])
        if not flag:
            self._managed = True

    def update(self, dt):
        super().update(dt)
        self.check_npc_distance()

    def take_exp(self, exp):
        exp_to_next = LEVELS_PROPERTIES[self.level]['exp_to_next']
        if self._exp + exp < exp_to_next:
            self._exp += exp
            print(self._exp)
            return False
        else:
            self._exp = self._exp+exp - exp_to_next
            self._new_level()
            print(self._exp)
            return True

    def set_health(self, new_value):
        self.health = new_value

    @property
    def exp(self):
        return self._exp


class CutscenePlayer(Player):
    def _input(self, dt):
        if self._managed:
            keys = pygame.key.get_pressed()

            # Горизонтальное движение
            if keys[pygame.K_a] and not keys[pygame.K_d]:
                self._direction.x = -1
                self._change_anim_status("walk_left")
            elif keys[pygame.K_d] and not keys[pygame.K_a]:
                self._direction.x = 1
                # self._change_anim_status("walk_right")
            else:
                self._direction.x = 0

            if self._direction.magnitude() == 0:
                self._change_anim_status("idle_down")
