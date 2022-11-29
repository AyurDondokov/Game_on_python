import pygame
from properties import *
from level import Level
"""Основной скелет игры, класс Game"""


class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("None")
        self.game_over = False
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.level = Level()

    def run(self):
        while not (self.game_over):
            for event in pygame.event.get():  # Блок с отловом событий в дальнейшем перекачует в отдельный метод класса Game
                if event.type == pygame.QUIT:
                    pygame.quit()
            self.screen.fill('black')
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == '__main__':
    game = Game()
    game.run()
