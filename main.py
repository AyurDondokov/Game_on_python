"""Основной скелет игры, класс Game"""
import pygame
from properties import *
from level import Level
from scene_manager import SceneManager
import logging
from menu import *


class Game:
    def __init__(self):
        """Инициализация pygame"""
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
            # запуск паузы
            # if self.K_ESCAPE:
            #     self.pause_def()
            self.window.fill('black')
            # delta time - время между кадрами, нужно для правильной работы движения
            dt = self.clock.tick(FPS) / 1000
            self.manager.run(dt)
            pygame.display.update()

    # def pause_def(self):
    #     self.pause_menu = True
    #     self.reset_keys()
    #     while self.pause_menu:
    #         for event in pygame.event.get():
    #             if event.type == pygame.QUIT:
    #                 pygame.quit()
    #                 sys.exit()
    #         keys = pygame.key.get_pressed()
    #         if keys[pygame.K_SPACE]:
    #             self.pause_menu = False
    #             self.K_ESCAPE = False
    #         self.window.blit(self.display, (0, 0))
    #         self.display.fill((0, 0, 0))
    #         self.draw_text("PAUSED", 85, self.SCREEN_WIDTH /
    #                        2, self.SCREEN_HEIGHT / 4 - 130)
    #         self.draw_text("Press SPACE for continue", 40,
    #                        self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT / 4 + 150)
    #         pygame.display.update()


if __name__ == '__main__':
    """Запуск игры"""

    # настройка логирования
    logging.basicConfig(level=logging.DEBUG,
                        filename="py_log.log", filemode="w",
                        format='%(levelname)s:%(filename)s:%(funcName)s:Line %(lineno)d:%(message)s')
    logging.info("Game starting...")

    game = Game()
    game.run()
