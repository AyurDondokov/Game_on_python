import pygame
class Menu():
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = - 100
        self.BACKGROUND_MENU = pygame.image.load('menu.jpg')
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
        self.exitx, self.exity = self.mid_w, self.mid_h + 170
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.blit(self.BACKGROUND_MENU, (0, 0))
            self.game.draw_text("Игра короч", 100, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 4)
            self.game.draw_text("START", 40, self.startx, self.starty)
            self.game.draw_text("OPTIONS", 40, self.optionsx, self.optionsy)
            self.game.draw_text("EXIT", 40, self.exitx, self.exity)
            self.draw_cursor()
            self.blit_screen()
    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == "START":
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = "OPTIONS"
            elif self.state == "OPTIONS":
                self.cursor_rect.midtop = (self.exitx + self.offset, self.exity)
                self.state = "EXIT"
            elif self.state == "OPTIONS":
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = "START"
        if self.game.UP_KEY:
            if self.state == "START":
                self.cursor_rect.midtop = (self.exitx + self.offset, self.exity)
                self.state = "EXIT"
            elif self.state == "OPTIONS":
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = "START"
            elif self.state == "EXIT":
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = "OPTIONS"
    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == 'START':
                self.game.playing = True
            elif self.state == 'OPTIONS':
                pass
            elif self.state == 'EXIT':
                pass
            self.run_display = False
class OptionsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Volume"
        self.volx, self.voly = self.mid_w, self.mid_h + 20