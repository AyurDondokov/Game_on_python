import pygame
import properties as pr


class Menu:
    def __init__(self, buttons,
                 action_bar_path: str = "./sprites/fight/UI/action_bar.png",
                 pos: tuple = pr.BATTLE_ACTIONS_BAR_POS):
        self._action_bar = pygame.sprite.Sprite()
        self._action_bar.image = pygame.image.load(action_bar_path)
        self._action_bar.rect = self._action_bar.image.get_rect(center=pos)
        self._target_index = 0

        self._buttons = buttons
        self._buttons_count = len(self._buttons)
        self._buttons[self._target_index].is_targeted = True

        self._display_surf = pygame.display.get_surface()
        self.__event_list = []
        self.sound_bt_hover = pygame.mixer.Sound('music_and_sound/sound/button/hover.mp3')

    def change_target_on_n(self, n):
        self._buttons[self._target_index].is_targeted = False
        self._target_index = n
        self._buttons[self._target_index].is_targeted = True

    def draw_menu(self):
        self._display_surf.blit(self._action_bar.image, self._action_bar.rect)
        for button in self._buttons:
            button.draw()

    def set_events_list(self, event_list):
        self.__event_list = event_list
        for button in self._buttons:
            button.set_events_list(event_list)

    def input(self):
        for event in self.__event_list:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.sound_bt_hover.play()
                    if self._target_index - 1 >= 0:
                        self.change_target_on_n(self._target_index - 1)
                    else:
                        self.change_target_on_n(self._buttons_count - 1)
                elif event.key == pygame.K_d:
                    self.sound_bt_hover.play()
                    if self._target_index + 1 < self._buttons_count:
                        self.change_target_on_n(self._target_index + 1)
                    else:
                        self.change_target_on_n(0)
                elif event.key == pygame.K_w:
                    self.sound_bt_hover.play()
                    if self._target_index - 1 >= 0:
                        self.change_target_on_n(self._target_index - 1)
                    else:
                        self.change_target_on_n(self._buttons_count - 1)
                elif event.key == pygame.K_s:
                    self.sound_bt_hover.play()
                    if self._target_index + 1 < self._buttons_count:
                        self.change_target_on_n(self._target_index + 1)
                    else:
                        self.change_target_on_n(0)

    def update(self):
        for button in self._buttons:
            button.update()


class Button:
    def __init__(self, func, args, pos,
                 # Настройки для кнопки изображения
                 image_path: str = "",
                 selected_image_path: str = "",
                 sprite_group: pygame.sprite.Group = None,
                 # Настройки для кнопки текста
                 text: str = "",
                 font_name: str = pr.FONT_NAME,
                 text_size: int = 28,
                 text_color: tuple = pr.WHITE,
                 selected_text_color: tuple = pr.BLACK):

        if len(image_path) != 0 and len(text) == 0:
            assert not sprite_group and len(selected_image_path) != 0
            self.__button_type = "image"
            self.__button_sprite = pygame.sprite.Sprite(sprite_group)
            self.__image = pygame.image.load(image_path)
            self.__button_sprite.image = self.__image
            self.__selected_image = pygame.image.load(selected_image_path)
            self.__button_sprite.rect = self.__button_sprite.image.get_rect(center=pos)
        elif len(image_path) == 0 and len(text) != 0:
            self.__button_type = "text"
            self.__font = pygame.font.Font(font_name, text_size)
            self.__text = text
            self.__selected_text_color = selected_text_color
            self.__text_color = text_color
            self.__text_surface = self.__font.render(self.__text, True, self.__text_color)
            self.__text_rect = self.__text_surface.get_rect(center=pos)
        elif len(image_path) != 0 and len(text) != 0:
            self.__button_type = "image_text"
            self.__button_sprite = pygame.sprite.Sprite(sprite_group)
            self.__image = pygame.image.load(image_path)
            self.__button_sprite.image = self.__image
            self.__selected_image = pygame.image.load(selected_image_path)
            self.__button_sprite.rect = self.__button_sprite.image.get_rect(center=pos)
            self.__font = pygame.font.Font(font_name, text_size)
            self.__text = text
            self.__selected_text_color = selected_text_color
            self.__text_color = text_color
            self.__text_surface = self.__font.render(self.__text, True, self.__text_color)
            self.__text_rect = self.__text_surface.get_rect(center=pos)
        else:
            raise ValueError('Button without type(image or text).')
        self.__is_targeted = False
        self.__function = func
        self.__args = args
        self.__display_surf = pygame.display.get_surface()
        self.__event_list = []

    def set_events_list(self, event_list):
        self.__event_list = event_list

    def input(self):
        for event in self.__event_list:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    if self.__is_targeted:
                        if self.__args:
                            self.__function(self.__args)
                        else:
                            self.__function()
    def update(self):
        if self.__button_type == "image":
            if not self.__is_targeted:
                self.__button_sprite.image = self.__image
            else:
                self.__button_sprite.image = self.__selected_image
        elif self.__button_type == "text":
            if not self.__is_targeted:
                self.__text_surface = self.__font.render(self.__text, True, self.__text_color)
            else:
                self.__text_surface = self.__font.render(self.__text, True, self.__selected_text_color)
        elif self.__button_type == "image_text":
            if not self.__is_targeted:
                self.__button_sprite.image = self.__image
                self.__text_surface = self.__font.render(self.__text, True, self.__text_color)
            else:
                self.__button_sprite.image = self.__selected_image
                self.__text_surface = self.__font.render(self.__text, True, self.__selected_text_color)

        self.input()

    def draw(self):
        if self.__button_type == "image":
            self.__display_surf.blit(self.__button_sprite.image, self.__button_sprite.rect)
        elif self.__button_type == "text":
            self.__display_surf.blit(self.__text_surface, self.__text_rect)
        elif self.__button_type == "image_text":
            self.__display_surf.blit(self.__button_sprite.image, self.__button_sprite.rect)
            self.__display_surf.blit(self.__text_surface, self.__text_rect)

    @property
    def type(self):
        return self.__button_type

    @property
    def is_targeted(self) -> bool:
        return self.__is_targeted

    @is_targeted.setter
    def is_targeted(self, new_value: bool):
        self.__is_targeted = new_value


class ProgressBar:
    def __init__(self, cord: tuple,
                 size: tuple = pr.BATTLE_PROG_BAR_SIZE,
                 color: tuple = pr.BATTLE_PROG_BAR_COLOR,
                 back_color: tuple = (0, 0, 0)):
        self.__cord = cord
        self.__size = size
        self.__color = color
        self.__back_color = back_color
        self.__position = [cord[0] + (size[0]/2), cord[1] + (size[1]/2)]
        self.__rect = [self.__position[0], self.__position[1], self.__size[0], self.__size[1]]
        self.__back_rect = [self.__position[0], self.__position[1], self.__size[0], self.__size[1]]
        self.__max_value = 1
        self.__value = 1

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value: float):
        assert 0.0 <= new_value <= 1.0, f"new_value: {new_value}"
        self.__value = new_value
        self.__rect[2] = self.__size[0] * (self.__value / self.__max_value)

    @property
    def rect(self):
        return self.__back_rect, self.__rect

    @property
    def color(self):
        return self.__back_color, self.__color


class PowerScale:
    def __init__(self,
                 bg_image_path: str = "./sprites/fight/UI/power_scale.png",
                 slider_image_path: str = "./sprites/fight/UI/power_scale_slider.png",
                 pos: tuple = pr.BATTLE_SLIDER_POS,
                 speed: int = pr.BATTLE_SLIDER_SPEED):
        self.__display_surf = pygame.display.get_surface()
        self.__event_list = []
        self.bg_image = pygame.image.load(bg_image_path)
        self.bg_rect = self.bg_image.get_rect(center=pos)
        self.slider_image = pygame.image.load(slider_image_path)
        self.slider_rect = self.slider_image.get_rect(bottomleft=self.bg_rect.bottomleft)
        self.slider_pos = pygame.math.Vector2(self.slider_rect.center)
        self.slider_speed = speed
        self.slider_x_direction = 1

    def get_value(self):
        half = self.bg_rect.width/2
        if self.slider_pos.x <= self.bg_rect.centerx:
            return (self.slider_pos.x - self.bg_rect.left) / half
        else:
            return (self.bg_rect.right - self.slider_pos.x) / half

    def slider_move(self, dt):
        if self.slider_rect.left <= self.bg_rect.left:
            self.slider_x_direction = 1
        elif self.slider_rect.right >= self.bg_rect.right:
            self.slider_x_direction = -1
        self.slider_pos.x += self.slider_x_direction * self.slider_speed * dt
        self.slider_rect.centerx = round(self.slider_pos.x)

    def update(self, dt):
        self.slider_move(dt)

    def draw(self):
        self.__display_surf.blit(self.bg_image, self.bg_rect)
        self.__display_surf.blit(self.slider_image, self.slider_rect)

