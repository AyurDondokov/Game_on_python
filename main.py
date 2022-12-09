"""Основной скелет игры, класс Game"""
import pygame
import sys
from properties import *
from level import Level
import logging
from menu import MainMenu
class Game():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("The best game ever")
        # Добавил menu_game
        self.game_over, self.menu_game = False, True
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False
        self.K_w, self.K_s = False, False

        # self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = 1080, 720
        self.display = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.window = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.font_name = './addons/monospace.ttf'
        self.WHITE = (255, 255, 255)
        self.clock = pygame.time.Clock()
        self.level = Level()
        self.main_menu = MainMenu(self)
        self.curr_menu = self.main_menu

    def run(self):
        while not self.game_over:
            self.events_update()
            if self.START_KEY:
                self.game_over = False
            self.window.fill('black')
            # delta time - время между кадрами, нужно для правильной работы движения
            dt = self.clock.tick(FPS) / 1000
            self.level.run(dt)
            pygame.display.update()
            self.reset_keys()

    def events_update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True
                if event.key == pygame.K_s:
                    self.K_s = True
                if event.key == pygame.K_w:
                    self.K_w = True
    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False
        self.K_s, self.K_w = False, False

    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        filename="py_log.log", filemode="w",
                        format='%(levelname)s:%(filename)s:%(funcName)s:Line %(lineno)d:%(message)s')
    logging.info("Game starting...")
    game = Game()
    game.run()
