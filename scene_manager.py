import pygame
from properties import *
from level import Level
import logging as log
from game_data import *


class SceneManager:
    """Класс управляющий отрисовкой уровней и меню"""

    def __init__(self):
        self.__levels_data = levels
        self.__current_level = 1
        self.__list_of_levels = []
        self.__levels_setup()

    def run(self, dt):
        self.__list_of_levels[self.__current_level].run(dt)

    def __levels_setup(self):
        for k in self.__levels_data:
            self.__list_of_levels.append(
                Level(self.__levels_data[k]["MAP"], self.set_current_level, self.__levels_data[k]["move_to"]))

    @property
    def current_level(self):
        return self.__current_level

    # @current_level.setter
    def set_current_level(self, value):
        self.__current_level = value
