import pygame
import sys


class Menu:
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = game.SCREEN_WIDTH / 2, game.SCREEN_HEIGHT / 2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = - 100
        self.BACKGROUND_MENU = pygame.image.load('./images/menu/menu.jpg')

    def draw_cursor(self):
        self.game.draw_text('->', 30, self.cursor_rect.x, self.cursor_rect.y)

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()


class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "START"
        self.startx, self.starty = self.mid_w, self.mid_h + 30
        self.optionsx, self.optionsy = self.mid_w, self.mid_h + 100
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 170
        self.exitx, self.exity = self.mid_w, self.mid_h + 250
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.events_update()
            self.check_input()
            self.game.display.blit(self.BACKGROUND_MENU, (0, 0))
            self.game.draw_text("Игра короч", 100, self.game.SCREEN_WIDTH / 2, self.game.SCREEN_HEIGHT / 4)
            self.game.draw_text("START", 40, self.startx, self.starty)
            self.game.draw_text("OPTIONS", 40, self.optionsx, self.optionsy)
            self.game.draw_text("CREDITS", 40, self.creditsx, self.creditsy)
            self.game.draw_text("EXIT", 40, self.exitx, self.exity)
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN_KEY or self.game.K_s:
            if self.state == "START":
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = "OPTIONS"
            elif self.state == "OPTIONS":
                self.cursor_rect.midtop = (self.exitx + self.offset, self.exity)
                self.state = "EXIT"
            elif self.state == "EXIT":
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = "START"
        if self.game.UP_KEY or self.game.K_w:
            if self.state == "START":
                self.cursor_rect.midtop = (self.exitx + self.offset, self.exity)
                self.state = "EXIT"
            elif self.state == "OPTIONS":
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = "START"
            elif self.state == "CREDITS":
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = "OPTIONS"
            elif self.state == "EXIT":
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsx)
                self.state = "CREDITS"

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == 'START':
                self.game.game_over = True
            elif self.state == 'OPTIONS':
                self.game.curr_menu = self.game.options
            elif self.state == 'CREDITS':
                self.game.curr_menu = self.game.credits
            elif self.state == 'EXIT':
                pass
            self.run_display = False


class OptionsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Volume"
        self.volx, self.voly = self.mid_w, self.mid_h + 20
        self.controlsx, self.controlsy = self.mid_w, self.mid_h + 40
        self.cursor_rect.midtop = (self.volx + self.offset, self.voly)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.events_update()
            self.game.display.fill('black')
            self.game.draw_text("OPRIONS", 85, self.game.SCREEN_WIDTH / 2, self.game.SCREEN_HEIGHT / 2 - 30)
            self.game.draw_text("Volume", 40, self.volx, self.voly)
            self.game.draw_text("Window", 40, self.controlsx, self.controlsy)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        elif self.game.UP_KEY or self.game.DOWN_KEY:
            if self.state == 'Volume':
                self.state = 'Window'
                self.cursor_rect.midtop = (self.controlsx + self.offset, self.controlsy)
            elif self.state == 'Window':
                self.state = 'Volume'
                self.cursor_rect.midtop = (self.volx + self.offset, self.voly)
        elif self.game.START_KEY:
            pass


class CreditsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.events_update()
            if self.game.START_KEY or self.game.BACK_KEY:
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            self.game.display.fill('black')
            self.game.draw_text("CREDITS", 20, self.game.SCREEN_WIDTH / 2, self.game.SCREEN_HEIGHT / 4 - 20)
            self.blit_screen()