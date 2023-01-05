import logging as log
import pygame
import sys

from properties import *


class Menu:
    """Абстрактный класс для меню"""

    def __init__(self):

        # полчение Surface главного окна
        self.display_surface = pygame.display.get_surface()

        self.mid_w, self.mid_h = SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = - 100
        self.BACKGROUND_MENU = pygame.image.load('./images/menu/menu.jpg')
        self.BACK_KEY = False
        self.DOWN_KEY = False
        self.UP_KEY = False
        self.K_s = False
        self.K_w = False
        self.K_ESCAPE = False
        self.START_KEY = False

    def events_update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
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
                if event.key == pygame.K_ESCAPE:
                    self.K_ESCAPE = True
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True

    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(FONT_NAME, size)
        text_surface = font.render(text, True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display_surface.blit(text_surface, text_rect)

    def draw_cursor(self):
        """Создание курсора навигации"""
        self.draw_text(
            '->', 30, self.cursor_rect.x, self.cursor_rect.y)

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False
        self.K_s, self.K_w = False, False
        self.K_ESCAPE = False


class MainMenu(Menu):
    """Основное меню"""

    def __init__(self, is_game_started, set_curr_menu):
        Menu.__init__(self)
        # переменные для переключения в scene_manager
        self.set_is_game_started = is_game_started
        self.set_current_menu = set_curr_menu
        # инициализация начального положения - на START
        self.state = "START"
        # Рисуем кнопку START
        self.startx, self.starty = self.mid_w, self.mid_h + 30
        # Рисуем кнопку OPTIONS
        self.optionsx, self.optionsy = self.mid_w, self.mid_h + 100
        # Рисуем кнопку CREDITS
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 170
        # Рисуем кнопку EXIT
        self.exitx, self.exity = self.mid_w, self.mid_h + 250
        # Рисуем кнопку курсор
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)

    def display_menu(self):
        self.run_display = True
        # Проверяет события
        self.events_update()
        # Проверяет, что выбрано
        self.check_input()
        # задний фон
        self.display_surface.blit(self.BACKGROUND_MENU, (0, 0))
        # Название игры на экране
        self.draw_text(
            " ", 100, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)
        # название 1 конпки
        self.draw_text("START", 40, self.startx, self.starty)
        # название 2 конпки
        self.draw_text("OPTIONS", 40, self.optionsx, self.optionsy)
        # название 3 конпки
        self.draw_text("CREDITS", 40, self.creditsx, self.creditsy)
        # название 4 конпки
        self.draw_text("EXIT", 40, self.exitx, self.exity)
        # Отрисовка курсора
        self.draw_cursor()

    def move_cursor(self):
        """Движение курсора"""
        # Если кнопка (Стрелка вниз) или S
        if self.DOWN_KEY or self.K_s:
            # С какой кнопки движение
            if self.state == "START":
                self.cursor_rect.midtop = (
                    self.optionsx + self.offset, self.optionsy)
                # На какую
                self.state = "OPTIONS"
            elif self.state == "OPTIONS":
                self.cursor_rect.midtop = (
                    self.creditsx + self.offset, self.creditsy)
                self.state = "CREDITS"
            elif self.state == "CREDITS":
                self.cursor_rect.midtop = (
                    self.exitx + self.offset, self.exity)
                self.state = "EXIT"
            elif self.state == "EXIT":
                self.cursor_rect.midtop = (
                    self.startx + self.offset, self.starty)
                self.state = "START"
        if self.UP_KEY or self.K_w:
            if self.state == "START":
                self.cursor_rect.midtop = (
                    self.exitx + self.offset, self.exity)
                self.state = "EXIT"
            elif self.state == "OPTIONS":
                self.cursor_rect.midtop = (
                    self.startx + self.offset, self.starty)
                self.state = "START"
            elif self.state == "CREDITS":
                self.cursor_rect.midtop = (
                    self.optionsx + self.offset, self.optionsy)
                self.state = "OPTIONS"
            elif self.state == "EXIT":
                self.cursor_rect.midtop = (
                    self.creditsx + self.offset, self.creditsx)
                self.state = "CREDITS"

    def check_input(self):
        """Проверка какая кнопка была выбрана"""
        # Движение курсора
        self.move_cursor()
        # Если выбрана кнопка
        if self.START_KEY:
            log.debug(f"button {self.START_KEY} was clicked")
            # Проверка какая
            if self.state == 'START':
                log.debug(f"button {self.state} was clicked")
                # Действие
                self.set_is_game_started(True)
            elif self.state == 'OPTIONS':
                log.debug(f"Options clicked")
                self.set_current_menu("options")
            elif self.state == 'CREDITS':
                self.set_current_menu("credits")
            elif self.state == 'EXIT':
                pygame.quit()
                sys.exit()
        self.reset_keys()


class OptionsMenu(Menu):
    def __init__(self, change_menu_f):
        Menu.__init__(self)
        self.set_current_menu = change_menu_f
        self.state = "Volume"
        self.volx, self.voly = self.mid_w, self.mid_h + 35
        self.controlsx, self.controlsy = self.mid_w, self.mid_h + 75
        self.cursor_rect.midtop = (self.volx + self.offset, self.voly)

    def display_menu(self):
        self.check_input()
        self.events_update()
        self.display_surface.fill('black')
        self.draw_text(
            "OPTIONS", 85, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 150)
        self.draw_text("Volume", 40, self.volx, self.voly)
        self.draw_text("Window", 40, self.controlsx, self.controlsy)
        self.draw_cursor()

    def check_input(self):
        if self.BACK_KEY:
            self.set_current_menu("main")
        elif self.UP_KEY or self.DOWN_KEY:
            if self.state == 'Volume':
                self.state = 'Window'
                self.cursor_rect.midtop = (
                    self.controlsx + self.offset, self.controlsy)
            elif self.state == 'Window':
                self.state = 'Volume'
                self.cursor_rect.midtop = (self.volx + self.offset, self.voly)
        elif self.START_KEY:
            pass
        self.reset_keys()


class CreditsMenu(Menu):
    """Конструктор окна Credits"""

    def __init__(self, change_menu_f):
        Menu.__init__(self)
        self.set_current_menu = change_menu_f

    def display_menu(self):
        self.events_update()
        if self.START_KEY or self.BACK_KEY:
            self.set_current_menu()
            self.reset_keys()

        self.display_surface.fill('black')
        self.draw_text(
            "CREDITS", 85, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4 - 130)
        self.draw_text(
            "Game made by:", 40, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4 - 70)
        self.draw_text("Andrew Gorohov - job", 30, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4 + 25)
        self.draw_text("Aur Dondokov - job", 30, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4 + 60)
        self.draw_text("Darya Vasylchyk - job", 30, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4 + 95)
        self.draw_text("Konstantin Harytkin - job", 30, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4 + 130)
        self.draw_text("Ksenya Zyranova - job", 30, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4 + 165)
        self.draw_text("Natalia Zueva - job", 30, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4 + 200)
        self.draw_text("Sofia Shadarova - job", 30, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4 + 235)
        self.draw_text("Yuri Verbitsky - job", 30, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4 + 270)
