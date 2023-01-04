import pygame
import logging as log
import sys

from properties import *


class HealthBar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # В LEVELS_PROPERTIES 1 словарь, где здоровье = 100
        # После прокачки level_health будет увеличен на единицу
        self.level_health = 1
        # Уровни здоровья, брони и урона
        self.health = LEVELS_PROPERTIES[self.level_health]['max_health']
        self.armor = LEVELS_PROPERTIES[self.level_health]['armor']
        self.damage = LEVELS_PROPERTIES[self.level_health]['max_damage']

    def takeDamage(self):
        self.health -= (self.damage - self.armor)
        if self.health < 0:
            self.health = 0

    def Heal(self, heal):
        self.health += heal
        if self.health > 5:
            self.health = 5