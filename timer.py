import pygame


class Timer:
    def __init__(self, duration, func = None):
        self.duration = duration
        self.__function = func
        self.start_time = 0
        self.active = False

    def activate(self):
        self.active = True
        self.start_time = pygame.time.get_ticks()

    def deactivate(self):
        self.active = False
        self.start_time = 0

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time >= self.duration:
            self.deactivate()
            if self.__function:
                self.__function()

    @property
    def function(self):
        return self.__function

    @function.setter
    def function(self, new_func):
        self.function = new_func
