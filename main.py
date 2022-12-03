import pygame, sys
from properties import *
from level import Level
"""Основной скелет игры, класс Game"""


class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("The best game ever")
        self.game_over = False
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.level = Level()

    def run(self):
        while not self.game_over:
            self.screen.fill('black')
            for event in pygame.event.get():  # Блок с отловом событий в дальнейшем перекачует в отдельный метод класса Game
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            dt = self.clock.tick(FPS) / 1000
            self.level.run(dt)
            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()
