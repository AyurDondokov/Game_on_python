
import pygame
from properties import *
from support import *
import logging as log
from copy import deepcopy


class GameObject(pygame.sprite.Sprite):
    """Абстрактный класс для всех игровых обьектов, кроме Tile`ов"""

    def __init__(self, position: tuple,
                 sprite_group: pygame.sprite.Group,
                 sprite_path: str,
                 z: int,
                 image_surf: pygame.surface.Surface = None,
                 hitbox_size: tuple = (0, 0),
                 hitbox_offset: tuple = (0, 0),
                 movement_speed: float = 0,
                 is_animated: bool = False,
                 anim_speed: float = DEFAULT_CHARACTER_ANIM_SPEED,
                 animations_pack: dict = STANDARD_OBJ_ANIM_PACK):
        super().__init__(sprite_group)

        # Настройки анимации
        self._is_animated = is_animated
        if self._is_animated:
            self._animations = deepcopy(animations_pack)
            self._anim_status = list(self._animations.keys())[0]  # Статус анимации
            self._anim_frame_index = 0  # Индекс кадра, на котором находится текущая анимация
            self._anim_speed = anim_speed  # Сколько секунд должно пройти для переключения кадра

        if not image_surf:
            self._import_assets(sprite_path)
        else:
            self.image = image_surf
            print(self.image)

        # Основные настройки
        self.rect = self.image.get_rect(topleft=position)
        self.hitbox = self.rect.copy().inflate(self.rect.width * hitbox_size[0] - self.rect.width,
                                               self.rect.height * hitbox_size[1] - self.rect.height)
        self.hitbox_offset = hitbox_offset
        self.hitbox.centerx = self.rect.centerx + \
            self.rect.width * self.hitbox_offset[0]
        self.hitbox.centery = self.rect.centery + \
            self.rect.height * self.hitbox_offset[1]
        self.z = z

        # Настройки передвижения
        self._direction = pygame.math.Vector2()
        self._pos = pygame.math.Vector2(self.rect.center)
        self._speed = movement_speed

    @property
    def speed(self):
        return self._speed

    @property
    def pos(self):
        return self._pos

    def _import_assets(self, path):
        """Функция для добавления всех анимаций персонажу"""
        if self._is_animated:
            for animation in self._animations.keys():
                full_path = path + animation
                self._animations[animation] = import_surfaces_from_folder(full_path)
            self.image = self._animations[self._anim_status][self._anim_frame_index]
        else:
            self.image = pygame.image.load(path).convert_alpha()

    def _input(self, dt):
        """Приём нажатия клавишь"""
        pass

    def _collision(self, direction):
        """Обработка столкновений"""
        self.hitbox.centerx = self.rect.centerx + \
            self.rect.width * self.hitbox_offset[0]
        self.hitbox.centery = self.rect.centery + \
            self.rect.height * self.hitbox_offset[1]

    def _move(self, dt):
        if self._speed != 0:
            if self._direction.magnitude() > 0:  # Нужно для того чтобы персонаж не ускорялся двигаясь по диагонали
                self._direction = self._direction.normalize()

            self._pos.x += self._direction.x * self._speed * dt
            self.hitbox.centerx = round(self._pos.x)
            self.rect.centerx = self.hitbox.centerx
            self._collision('horizontal')

            self._pos.y += self._direction.y * self._speed * dt
            self.hitbox.centery = round(self._pos.y)
            self.rect.centery = self.hitbox.centery
            self._collision('vertical')

    def _change_anim_status(self, new_state: str):
        self._anim_status = new_state

    def _animate(self, dt):
        """Смена кадров анимации"""
        self._anim_frame_index += 1 / \
            self._anim_speed[self._anim_status.split("_", 1)[0]] * dt
        if self._anim_frame_index >= len(self._animations[self._anim_status]):
            self._anim_frame_index = 0
        self.image = self._animations[self._anim_status][int(
            self._anim_frame_index)]

    def locate(self, pos):
        "меняет расположение обьекта"
        self._pos.x = pos[0]
        self._pos.y = pos[1]
        self.rect = self.image.get_rect(center=pos)

    def update(self, dt):
        self._input(dt)
        self._move(dt)
        if self._is_animated:
            self._animate(dt)
