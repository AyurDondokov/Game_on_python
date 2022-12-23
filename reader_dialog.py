class ReadingLocations:
    """"Класс для работы с диалогами из файла

        формат:
        ===location=== (указатель на блок текста,локация)
        основной блок текста
        (выборка:)
        + None: *текст* -> location (переход)
        + None: *текст* -> location (переход)
    """

    def __init__(self, title):
        """
        self.conversation list содержит основной блок текста
        self.choise list содержит блок выборки
        self.title = содержит документ .txt
        self.__dict_of_locations словарь из локаций {локация: (start, end)} - индексы строк диалога
        self.__dict_of_locations_select словарь из выбора по локациямлокаций {выбор: локация}
        self.__dictionary_of_locations list массив индексов строк локаций (=== loc ===)
        self.__listing_locations = []  # массив из локаций
        """
        self.conversation, self.choice = [], []
        self.title = title
        self.__dict_of_locations = {}
        self.__dict_of_locations_select = {}
        self.__dictionary_of_locations = []
        self.__listing_locations = []
        self.dialog = None
        self.lines = ()
        #чтение диалога
        self.reader()

    def reader(self):
        """Чтение файла и первоначальная обработка"""
        with open(self.title, 'r', encoding="utf-8") as file:
            self.lines = file.readlines()
            for line in self.lines:
                if line.startswith('==='):
                    if not line.startswith('=== +'):
                        self.__dictionary_of_locations.append(self.lines.index(line))
                        example = {line.rstrip()[4:-4]: None}
                        self.__dict_of_locations.update(example)
                    # else:
                    #     self.__dict_of_locations_select

            self.__dictionary_of_locations.append(len(self.lines))
            self.__listing_locations = list(self.__dict_of_locations)
            for i in range(len(self.__dict_of_locations)):
                self.__dict_of_locations[self.__listing_locations[i]] = \
                    [self.__dictionary_of_locations[i], self.__dictionary_of_locations[i + 1]]

    def dia_loc(self, loc):
        """Вызов диалога определенной локации"""
        start, end = self.__dict_of_locations[loc]
        dialogue = self.lines[start + 1:end - 1]
        self.dialog = []
        for line in dialogue:
            self.dialog.append(line.rstrip())
        self.selection()
        return self.conversation

    def selection(self):
        """Разделение обычного диалога и выбора сценария при наличии"""
        i = 0
        self.conversation, self.choice = [], []
        while i < len(self.dialog):
            if self.dialog[i][0:1] != '+':
                self.conversation.append(self.dialog[i])
            elif self.dialog[i][0:1] == '+':
                if i < len(self.dialog) - 1 and self.dialog[i + 1][0:1] == '+':
                    self.choice.append(self.dialog[i][2:])
            i += 1
        if self.dialog[i - 1][0:1] == '+':
            self.choice.append(self.dialog[len(self.dialog) - 1][2:])

        # self.checking_the_selection()

    # @property
    # def conversation(self):
    #     return self.conversation
    #
    # @property.setter
    # def conversation(self, value):
    #     self.conversation = value

    # def checking_the_selection(self):
    #     if self.choice == []:
    #         print('\n')
    #         for i in range(len(self.conversation)):
    #             print(self.conversation[i])
    #     else:
    #         print('\n')
    #         for i in range(len(self.conversation)):
    #             print(self.conversation[i])
    #         for i in self.choice:
    #             print(i)
    #             monologue, state = i.split("->")
    #         if state != 'END':
    #             self.dia_loc(f'{state.strip()}')

    @property
    def location_dialog(self):
        return self.__dict_of_locations

    @property
    def array_location(self):
        return self.__listing_locations
