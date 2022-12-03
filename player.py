import pygame
from properties import *


class Player(pygame.sprite.Sprite):
    def __init__(self, position, sprite_group):
        super().__init__(sprite_group)

        # Основные настройки
        self.image = pygame.Surface((32, 64))
        self.image.fill('green')
        self.rect = self.image.get_rect(center=position)

        # Настройки передвижения
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 200

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w] and not keys[pygame.K_s]:
            self.direction.y = -1
        elif keys[pygame.K_s] and not keys[pygame.K_w]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_a] and not keys[pygame.K_d]:
            self.direction.x = -1
        elif keys[pygame.K_d] and not keys[pygame.K_a]:
            self.direction.x = 1
        else:
            self.direction.x = 0

        print(self.direction)

    def move(self, dt):
        self.pos += self.direction * self.speed * dt
        self.rect.center = self.pos

    def update(self, dt):
        self.input()
        self.move(dt)
