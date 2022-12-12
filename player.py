"""Модуль, где описан класс игрока"""
import pygame
from properties import *
from support import *
from game_object import GameObject
import logging as log


class Player(GameObject):
    def __init__(self, position: tuple[float, float],
                 sprite_group: pygame.sprite.Group,
                 collision_sprites: pygame.sprite.Group,
                 interactable_sprites: pygame.sprite.Group):
        super().__init__(position, sprite_group,
                         "./sprites/main_character/", LAYERS['player'], (
                             0, 0.25), DEFAULT_CHARACTER_SPEED, True,
                         DEFAULT_CHARACTER_ANIM_SPEED, STANDARD_CHARACTER_ANIM_PACK)
        self.hitbox = self.rect.copy().inflate(-self.rect.width *
                                               0.2, -self.rect.height * 0.5)
        self.collision_sprites = collision_sprites
        self.interactable_sprites = interactable_sprites
        self.time_for_click_again = TIME_BETWEEN_INTERACT

    def _collision(self, direction):
        super(Player, self)._collision(direction)
        for sprite in self.collision_sprites:
            if hasattr(sprite, 'hitbox'):
                if sprite.hitbox.colliderect(self.hitbox):
                    if hasattr(sprite, 'trigger'):
                        # Проверка на тригер
                        sprite.check()
                    if direction == 'horizontal':
                        if self.direction.x > 0:
                            self.hitbox.right = sprite.hitbox.left
                        if self.direction.x < 0:
                            self.hitbox.left = sprite.hitbox.right

                        self.rect.centerx = self.hitbox.centerx - \
                            self.rect.width * self.hitbox_offset[0]
                        self.pos.x = self.hitbox.centerx - \
                            self.rect.width * self.hitbox_offset[0]

                    if direction == 'vertical':
                        if self.direction.y > 0:
                            self.hitbox.bottom = sprite.hitbox.top
                        if self.direction.y < 0:
                            self.hitbox.top = sprite.hitbox.bottom

                        self.rect.centery = self.hitbox.centery - \
                            self.rect.height * self.hitbox_offset[1]
                        self.pos.y = self.hitbox.centery - \
                            self.rect.height * self.hitbox_offset[1]

    def _input(self, dt):
        """Приём нажатия клавишь"""
        keys = pygame.key.get_pressed()

        # Вертикальное движение
        if keys[pygame.K_w] and not keys[pygame.K_s]:
            self.direction.y = -1
            self._change_anim_status("walk_up")
        elif keys[pygame.K_s] and not keys[pygame.K_w]:
            self.direction.y = 1
            self._change_anim_status("walk_down")
        else:
            self.direction.y = 0

        # Горизонтальное движение
        if keys[pygame.K_a] and not keys[pygame.K_d]:
            self.direction.x = -1
            self._change_anim_status("walk_left")
        elif keys[pygame.K_d] and not keys[pygame.K_a]:
            self.direction.x = 1
            self._change_anim_status("walk_right")
        else:
            self.direction.x = 0

        if self.direction.magnitude() == 0:
            self._change_anim_status("idle_" + self.anim_status.split('_')[1])

        if self.time_for_click_again > 0:
            self.time_for_click_again -= dt
        else:
            if keys[pygame.K_SPACE]:
                for sprite in self.interactable_sprites:
                    if hasattr(sprite, 'is_dialog_able'):
                        if sprite.is_dialog_able:
                            sprite.dialog.next_replica()
                            self.time_for_click_again = TIME_BETWEEN_INTERACT

    def check_npc_distance(self):
        for sprite in self.interactable_sprites:
            if hasattr(sprite, 'is_dialog_able'):
                sprite.is_dialog_able = self.pos.distance_to(
                    sprite.pos) < DISTANCE_FOR_INTERACT

    def update(self, dt):
        super().update(dt)
        self.check_npc_distance()
