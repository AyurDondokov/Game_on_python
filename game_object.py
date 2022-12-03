"""Модуль, где описан класс игрового объекта"""
import pygame
from properties import *
from support import *


class GameObject(pygame.sprite.Sprite):
    def __init__(self, position: tuple, sprite_group: pygame.sprite.Group, sprite_path: str, layer: int,
                 movement_speed: float = 0,
                 is_animated: bool = False,
                 anim_speed: float = DEFAULT_CHARACTER_ANIM_SPEED,
                 animations_pack: dict = STANDARD_OBJ_ANIM_PACK):
        super().__init__(sprite_group)

        # Настройки анимации
        self._is_animated = is_animated
        self.animations = animations_pack
        self.anim_status = list(self.animations.keys())[0]  # Статус анимации
        self.anim_frame_index = 0  # Индекс кадра, на котором находится текущая анимация
        self.anim_speed = anim_speed  # Сколько секунд должно пройти для переключения кадра

        self._import_assets(sprite_path)

        # Основные настройки
        self.rect = self.image.get_rect(center=position)
        self.z = layer

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

    def _move(self, dt):
        if self.direction.magnitude() > 0:  # Нужно для того чтобы персонаж не ускорялся двигаясь по диагонали
            self.direction = self.direction.normalize()

        self.pos += self.direction * self.speed * dt
        self.rect.center = self.pos

    def _animate(self, dt):
        self.anim_frame_index += 1 / self.anim_speed * dt
        if self.anim_frame_index >= len(self.animations[self.anim_status]):
            self.anim_frame_index = 0

        self.image = self.animations[self.anim_status][int(self.anim_frame_index)]

    def update(self, dt):
        self._input()
        self._move(dt)
        if self._is_animated:
            self._animate(dt)
