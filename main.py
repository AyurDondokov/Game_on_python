"""Основной скелет игры, класс Game"""
import logging

import pygame.mixer

from menu import *
from scene_manager import SceneManager


class Game:
    def __init__(self):
        """Инициализация pygame"""
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.init()
        pygame.display.set_caption("The best game ever")
        self.game_over, self.pause_menu = False, False
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = SCREEN_WIDTH, SCREEN_HEIGHT
        self.display = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.window = pygame.display.set_mode(
            (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        self.clock = pygame.time.Clock()
        self.manager = SceneManager()

    def run(self):
        """Основной цикл игры"""
        while not self.game_over:
            self.window.fill('black')
            # delta time - время между кадрами, нужно для правильной работы движения
            dt = self.clock.tick(FPS) / 1000
            self.manager.run(dt)
            pygame.display.update()


if __name__ == '__main__':
    """Запуск игры"""

    # настройка логирования
    logging.basicConfig(level=logging.DEBUG,
                        filename="py_log.log", filemode="w",
                        format='%(levelname)s:%(filename)s:%(funcName)s:Line %(lineno)d:%(message)s')
    logging.info("Game starting...")

    game = Game()
    game.run()
