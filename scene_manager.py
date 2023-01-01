import pygame
from properties import *
from level import Level
import logging as log
from game_data import *
from menu import *


class SceneManager:
    """Класс управляющий отрисовкой уровней и меню"""

    def __init__(self):
        # публичные переменные
        self.is_game_started = False
        # закрытые переменные
        self.__levels_data = levels

        self.__current_level = 0
        self.__current_menu = "main"

        self.__list_of_levels = []
        self.__dict_of_menus = {}
        # иницициализация меню и уровней
        self.__levels_setup()
        self.__menus_setup()

    def run(self, dt):
        """Переключает уровни, меню в зависимости от
         указателей  self.__current_level и self.__current_menu"""
        if self.is_game_started == True:
            self.__list_of_levels[self.__current_level].run(dt)
        else:
            self.__dict_of_menus[self.__current_menu].display_menu()

    def __levels_setup(self):
        """Создание массива с экземплярами уровней"""
        for k in self.__levels_data:
            self.__list_of_levels.append(
                Level(self.__levels_data[k], self.set_current_level))

    def __menus_setup(self):
        """
        Создает словарь с экземплярами меню
        Внутрь передаются функции меняющие указатель на текующее меню
        Внутри экземпляров эти функции вызываются, при нажатии клавиши
        """
        self.__dict_of_menus.update(
            {
                "main": MainMenu(self.set_is_game_started, self.set_current_menu),
                "options": OptionsMenu(lambda main="main": self.set_current_menu(main)),
                "credits": CreditsMenu(lambda main="main": self.set_current_menu(main)),
            })

    @property
    def current_level(self):
        return self.__current_level

    # @current_level.setter
    def set_current_level(self, value):
        self.__list_of_levels[self.current_level].is_runned = False

        self.__current_level = value

    def set_current_menu(self, value):
        log.debug(f"menu changed to {value}")
        self.__current_menu = value

    def set_is_game_started(self, value):
        self.is_game_started = value
