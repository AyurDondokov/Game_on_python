from properties import *
from support import *


class Text:
    """
    Класс для отрисовки текста
    на вход подаётся text
    """

    def __init__(self, screen, text, position, size, color):
        self.__screen = screen
        self.__cord = position
        self.__color = color
        self.__font = pygame.font.Font(None, size)
        self.__text = self.__font.render(text, False, color)  # -> Surface

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

    def __init__(self, dialog_replicas, position: tuple = DIALOG_WINDOW_POSITION):
        super().__init__()
        self.display_surf = pygame.display.get_surface()
        self.is_open = False
        self.selection = []

        # подложка диалога
        self.window = pygame.sprite.Sprite(self)
        self.window.image = pygame.image.load('./sprites/dialog_window.png')
        self.window.rect = self.window.image.get_rect(center=position)

        # аватарка говорящего
        self.npc_profile = pygame.sprite.Sprite(self)
        self.npc_profile.image = pygame.image.load('./sprites/dialog_person_test.png')
        self.npc_profile.rect = self.npc_profile.image.get_rect(bottomleft=self.window.rect.bottomleft)

        # реплики персонажей
        self.replicas = dialog_replicas
        self.replica_index = 0
        self.text_replica = Text(screen=self.display_surf,
                                 text=self.replicas[self.replica_index].split(':')[1],
                                 position=(self.npc_profile.rect.right, self.window.rect.centery),
                                 size=40,
                                 color=(0, 0, 0, 255))
        # имя говорящего
        self.text_name = Text(screen=self.display_surf,
                              text=self.replicas[self.replica_index].split(':')[0],
                              position=(self.npc_profile.rect.right, self.window.rect.centery - 80),
                              size=40,
                              color=(0, 0, 0, 255))

    def next_npc_profile(self):
        # +1
        pass

    def next_replica(self):
        """Отображение следущей реплики, пока таковые остались в списке"""
        if not self.is_open:
            self.is_open = True

        if self.replica_index < len(self.replicas):

            if not self.replicas[self.replica_index].startswith('+'):
                self.text_replica.text = self.replicas[self.replica_index].split(':')[1]
                # s = ''
                # for i in self.replicas[self.replica_index].split(':')[1]:
                #     s += i
                #     self.text_replica.text = s
                #     time.sleep(0.03)
                #     self.text_replica.out()
                #     print(s)
                # print(self.text_replica.text)  # <Surface(963x28x8 SW)>
                self.text_name.text = self.replicas[self.replica_index].split(':')[0]
                self.replica_index += 1
            else:
                self.text_name.text = None
                self.text_replica.text = self.replicas[self.replica_index].split('+')[1].split('->')[0]
                self.selection.append(self.replicas[self.replica_index].split('+')[1].split('->')[0])
                self.replica_index += 1
            # print(self.selection)
        else:
            self.is_open = False
            self.replica_index = 0

    def custom_draw(self):
        if self.is_open:
            self.display_surf.blit(self.window.image, self.window.rect)
            self.display_surf.blit(self.npc_profile.image, self.npc_profile.rect)
            self.text_replica.out()
            self.text_name.out()

    def update(self, dt):
        self.custom_draw()
