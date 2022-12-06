"""Основной скелет игры, класс Game"""
import pygame
import sys
from properties import *
from level import Level
import logging


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("The best game ever")
        self.game_over = False
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.level = Level()

    def run(self):
        while not self.game_over:
            self.screen.fill('black')
            self.events_update()

            # delta time - время между кадрами, нужно для правильной работы движения
            dt = self.clock.tick(FPS) / 1000
            self.level.run(dt)
            pygame.display.update()

    def events_update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        filename="py_log.log", filemode="w", format='%(levelname)s:%(filename)s:%(funcName)s:Line %(lineno)d:%(message)s')
    logging.info("Game starting...")
    game = Game()
    game.run()
