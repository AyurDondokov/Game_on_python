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
        # НЕизменяемая шкала здоровья
        self.health = LEVELS_PROPERTIES[self.level_health]['max_health']
        # Изменяемая шкала здоровья
        self.health_bar = LEVELS_PROPERTIES[self.level_health]['max_health']
        # Броня
        self.armor = LEVELS_PROPERTIES[self.level_health]['armor']
        # Урон
        self.damage = LEVELS_PROPERTIES[self.level_health]['max_damage']
        # Лечение
        self.heal = 25

        # Отрисовка шкалы здоровья (Уровень самого здоровья)
        # pygame.draw.rect(window, (60, 255, 15), (15, 30, health_bar, 25))
        # Отрисовка шкалы здоровья (Заполненная шкала)
        # pygame.draw.rect(window, (255, 255, 255), (15, 30, self.health, 25))

    # Функция в случае если игрок проиграл
    def game_over(self):
        pass

    # Нанесение дамага
    def takeDamage(self):
        self.health_bar -= (self.damage - self.armor)
        if self.health_bar < 0:
            self.health_bar = 0
            self.game_over()

    # Лечение
    def Heal(self):
        self.health_bar += self.heal
        if self.health_bar >= self.health_bar:
            self.health_bar = self.health_bar
