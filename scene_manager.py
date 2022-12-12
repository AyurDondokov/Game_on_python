import pygame
from properties import *
from level import Level
import logging as log
from game_data import *


class SceneManager:
    def __init__(self):
        self.levels_data = levels
        self.current_level = 1
        self.list_of_levels = []
        self.levels_setup()

    def run(self, dt):
        self.list_of_levels[self.current_level].run(dt)

    def levels_setup(self):
        for k in self.levels_data:
            self.list_of_levels.append(Level(self.levels_data[k]["MAP"]))
