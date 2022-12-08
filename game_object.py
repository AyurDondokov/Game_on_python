"""Модуль, где описан класс игрового объекта"""
import pygame
from properties import *
from support import *
import logging as log
from copy import deepcopy


class GameObject(pygame.sprite.Sprite):
    def __init__(self, position: tuple, sprite_group: pygame.sprite.Group, sprite_path: str, z: int,
                 hitbox_offset: tuple = (0, 0),
                 movement_speed: float = 0,
                 is_animated: bool = False,
                 anim_speed: float = DEFAULT_CHARACTER_ANIM_SPEED,
                 animations_pack: dict = STANDARD_OBJ_ANIM_PACK):
        super().__init__(sprite_group)

        # Настройки анимации
        self._is_animated = is_animated
        self.animations = deepcopy(animations_pack)
        self.anim_status = list(self.animations.keys())[0]  # Статус анимации
        self.anim_frame_index = 0  # Индекс кадра, на котором находится текущая анимация
        self.anim_speed = anim_speed  # Сколько секунд должно пройти для переключения кадра

        self._import_assets(sprite_path)
        # print(self.animations)

        # Основные настройки
        self.rect = self.image.get_rect(center=position)
        self.hitbox = self.rect.copy()
        self.hitbox_offset = hitbox_offset
        self.z = z

        # Настройки передвижения
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = movement_speed

    def _import_assets(self, path):
        """Функция для добавления всех анимаций персонажу"""
        if self._is_animated:
            for animation in self.animations.keys():
                full_path = path + animation
                self.animations[animation] = import_folder(full_path)
            self.image = self.animations[self.anim_status][self.anim_frame_index]
        else:
            self.image = pygame.image.load(path).convert_alpha()

    def _input(self):
        """Приём нажатия клавишь"""
        pass

    def _collision(self, direction):
        self.hitbox.centerx = self.rect.centerx + self.rect.width * self.hitbox_offset[0]
        self.hitbox.centery = self.rect.centery + self.rect.height * self.hitbox_offset[1]

    def _move(self, dt):
        if self.direction.magnitude() > 0:  # Нужно для того чтобы персонаж не ускорялся двигаясь по диагонали
            self.direction = self.direction.normalize()

        self.pos.x += self.direction.x * self.speed * dt
        self.hitbox.centerx = round(self.pos.x)
        self.rect.centerx = self.hitbox.centerx
        self._collision('horizontal')

        self.pos.y += self.direction.y * self.speed * dt
        self.hitbox.centery = round(self.pos.y)
        self.rect.centery = self.hitbox.centery
        self._collision('vertical')

    def _change_anim_status(self, new_state: str):
        self.anim_status = new_state

    def _animate(self, dt):
        self.anim_frame_index += 1 / \
            self.anim_speed[self.anim_status.split("_", 1)[0]] * dt
        if self.anim_frame_index >= len(self.animations[self.anim_status]):
            self.anim_frame_index = 0
        self.image = self.animations[self.anim_status][int(
            self.anim_frame_index)]

    def update(self, dt):
        self._input()
        self._move(dt)
        if self._is_animated:
            self._animate(dt)
