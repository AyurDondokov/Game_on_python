from properties import *
from support import *
from dialog.dialog_data import DIALOG_ICONS


class Text:
    """
    Класс для отрисовки текста
    на вход подаётся text
    """

    def __init__(self, screen, text, position, size, color):
        self.__screen = screen
        self.__cord = position
        self.__color = color
        self.__font = pygame.font.Font('addons/Roboto-Regular.ttf', size)
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
    """Класс отрисовки диалогов, кнопок в диалогах и тп"""

    def __init__(self, dialog_replicas, notify_func=None, position: tuple = DIALOG_WINDOW_POSITION):
        super().__init__()
        self.display_surf = pygame.display.get_surface()
        self.is_open = False
        self.selection = []
        self.notify_func = notify_func
        # подложка диалога
        self.window = pygame.sprite.Sprite(self)
        self.window.image = pygame.image.load('./sprites/dialog_window.png')
        self.window.rect = self.window.image.get_rect(center=position)

        # аватарка говорящего
        self.npc_profile = pygame.sprite.Sprite(self)
        self.npc_profile.image = pygame.image.load('./sprites/dialog_person_test.png')
        self.npc_profile.rect = self.npc_profile.image.get_rect()
        self.npc_profile.rect.centerx = self.window.rect.right
        self.npc_profile.rect.bottom = self.display_surf.get_rect().bottom

        # реплики персонажей
        self.replicas = dialog_replicas
        self.replica_index = 0
        self.text_replica = Text(screen=self.display_surf,
                                 text=self.replicas[self.replica_index].split(':')[1],
                                 position=(self.window.rect.x + 15, self.window.rect.top + 60),
                                 size=24,
                                 color=(255, 255, 255, 255))
        self.second_line = Text(screen=self.display_surf,
                                text="",
                                position=(self.window.rect.x + 15, self.window.rect.top + 100),
                                size=24,
                                color=(255, 255, 255, 255))
        # имя говорящего
        self.text_name = Text(screen=self.display_surf,
                              text=self.replicas[self.replica_index].split(':')[0],
                              position=(self.window.rect.x + 20, self.window.rect.top + 10),
                              size=24,
                              color=(255, 255, 255, 255))

    def change_npc_icon(self, char, value: str):

        surface = DIALOG_ICONS[char][value]
        self.npc_profile.image = surface

    def next_replica(self):
        """Отображение следущей реплики, пока таковые остались в списке"""
        if not self.is_open:
            self.is_open = True

        if self.replica_index < len(self.replicas):

            if not self.replicas[self.replica_index].startswith('+'):
                text_name = self.replicas[self.replica_index].split(':')[0]
                self.text_name.text = text_name
                if (pos_icon := text_name.find("|")) != -1:
                    self.change_npc_icon(text_name[:pos_icon], text_name[pos_icon+1:])
                    self.text_name.text = text_name[:pos_icon]
                else:
                    self.change_npc_icon(text_name, "idle")
                if self.replicas[self.replica_index].find("\\n") > 0:
                    splited = self.replicas[self.replica_index].split('\\n', 1)
                    self.text_replica.text = splited[0].split(':')[1]
                    self.second_line.text = splited[1]
                    self.replica_index += 1
                else:
                    self.second_line.text = ""
                    self.text_replica.text = self.replicas[self.replica_index].split(':')[1]
                    # s = ''
                    # for i in self.replicas[self.replica_index].split(':')[1]:
                    #     s += i
                    #     self.text_replica.text = s
                    #     time.sleep(0.03)
                    #     self.text_replica.out()
                    #     print(s)
                    # print(self.text_replica.text)  # <Surface(963x28x8 SW)>

                    self.replica_index += 1
            else:
                self.text_name.text = "None"
                replica = self.replicas[self.replica_index].split('+')[1]
                self.text_replica.text = replica.split('->')[0]
                self.replica_index = 0
                self.is_open = False
                self.notify_func(replica.split('->')[1])

            # print(self.selection)
        else:
            self.is_open = False
            self.replica_index = 0

    def custom_draw(self):
        if self.is_open:
            self.display_surf.blit(self.window.image, self.window.rect)
            self.display_surf.blit(self.npc_profile.image, self.npc_profile.rect)
            self.text_replica.out()
            self.second_line.out()
            self.text_name.out()

    def update_loc(self, new_loc):
        self.replicas = new_loc

    def update(self, dt):
        self.custom_draw()
