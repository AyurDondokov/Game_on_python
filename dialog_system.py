import pygame

import character
from properties import *
from support import *
from game_object import GameObject


class Text:
    def __init__(self, screen, text, position, size, color):
        self.__screen = screen
        self.__cord = position
        self.__color = color
        self.__font = pygame.font.Font(None, size)
        self.__text = self.__font.render(text, False, color)

    def out(self):
        self.__screen.blit(self.__text, self.__cord)

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, text):
        self.__text = self.__font.render(text, False, self.__color)

    def change_text(self, text):
        self.__text = self.__font.render(text, False, self.__color)


class Dialog(pygame.sprite.Group):
    def __init__(self, dialog_replicas, position: tuple = DIALOG_WINDOW_POSITION):
        super().__init__()
        self.display_surf = pygame.display.get_surface()
        self.is_open = False

        self.window = pygame.sprite.Sprite(self)
        self.window.image = pygame.image.load('./sprites/dialog_window.png')
        self.window.rect = self.window.image.get_rect(center=position)

        self.npc_profile = pygame.sprite.Sprite(self)
        self.npc_profile.image = pygame.image.load('./sprites/dialog_person_test.png')
        self.npc_profile.rect = self.npc_profile.image.get_rect(bottomleft=self.window.rect.bottomleft)

        self.replicas = dialog_replicas
        self.replica_index = 0
        self.text_replica = Text(screen=self.display_surf,
                                 text=self.replicas[self.replica_index].split(':')[1],
                                 position=(self.npc_profile.rect.right, self.window.rect.centery),
                                 size=40,
                                 color=(0, 0, 0, 255))

    def next_replica(self):
        if not self.is_open:
            self.is_open = True
        if self.replica_index < len(self.replicas):
            self.text_replica.text = self.replicas[self.replica_index].split(':')[1]
            self.replica_index += 1
        else:
            self.is_open = False
            self.replica_index = 0

    def custom_draw(self):
        if self.is_open:
            self.display_surf.blit(self.window.image, self.window.rect)
            self.display_surf.blit(self.npc_profile.image, self.npc_profile.rect)
            self.text_replica.out()

    def update(self, dt):
        self.custom_draw()
