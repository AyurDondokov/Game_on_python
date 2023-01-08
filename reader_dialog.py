class ReadingLocations:
    """"Класс для работы с диалогами из файла

        формат файла:
        ===location=== (указатель на блок текста, локация для диалога)
        основной блок текста
        Name: *text*

        На выходе получаем словарь
        {npc1: [{loc1: [text]}, {loc2: [text]}], npc2...}
    """

    def __init__(self, title: str):
        """
        self.title = содержит документ .txt

        основная логика*
        self.__dict_npc_loc -> dict основной словарь  {npc1: [{loc1: [text]}, {loc2: [text]}], npc2...}
        self.__dict_of_locations_select словарь из выбора по локациямлокаций {выбор: локация}
        self.__dictionary_of_locations -> list массив индексов строк локаций (=== loc ===)
        self.__listing_locations = []  # массив из локаций
        self.__dict_of_locations -> dict -  словарь из локаций {loc: (start, end)} - индексы строк диалога

        дополнительно*
        elf.lines = () - чтение всех линий файла
        self.mac = {} словарь {loc1: [text], loc2: [text]}
        self.dialog = [] - массив читорый сохраняет текст от начала до конца из {loc: (start, end)}
        """
        self.title = title
        self.__dict_npc_loc = {}
        self.__dict_of_locations_select = {}
        self.__dictionary_of_locations = []
        self.__listing_locations = []
        self.__dict_of_locations = {}
        self.lines = ()
        self.mac = {}
        self.dialog = []
        # чтение диалогого файла
        self.reader()

    def reader(self):
        """ Первоначальное чтение файла

        читает файл построчно заносит сведенья:
            1. всех npc данного мира - *self.__dict_npc_loc
            2. массив из данных строк: начала и конца диалогов - self.__dict_of_locations
            3. массив из всех локаций мира - self.__listing_locations
        """
        with open(self.title, 'r', encoding="utf-8") as file:
            self.lines = file.readlines()
            for line in self.lines:
                if line.startswith('==='):
                    self.__dictionary_of_locations.append(self.lines.index(line))
                    example = {line.rstrip()[4:-4]: None}
                    self.__dict_of_locations.update(example)

                    name_loc = line.rstrip()[4:-4]
                    npc = name_loc.split('__')[0]
                    name_npc = {npc: None}
                    self.__dict_npc_loc.update(name_npc)

            self.__dictionary_of_locations.append(len(self.lines))
            self.__listing_locations = list(self.__dict_of_locations)
            for i in range(len(self.__dict_of_locations)):
                self.__dict_of_locations[self.__listing_locations[i]] = \
                    [self.__dictionary_of_locations[i], self.__dictionary_of_locations[i + 1]]
        #
        self.mac_red()

    def mac_red(self) -> dict:
        """"
        Метод который пополняет уже созданный словарь:
        к каждому ключу npc представляется значение (массив)
        в котором впредставлены словари - {loc: *text*}
        """
        for name in (*self.__dict_npc_loc,):
            self.__dict_of_locations_select = {}
            self.mac = {}
            for i in self.__listing_locations:
                if i.startswith(name):
                    nut = i.split('__')[1]
                    example = {nut: self.dia_loc(i)}
                    self.mac.update(example)
            self.__dict_npc_loc.update({name: self.mac})

    def dia_loc(self, loc: str) -> list:
        """Вызов диалога определенной локации - возвращает массив реплик"""
        start, end = self.__dict_of_locations[loc]
        dialogue = self.lines[start + 1:end - 1]
        self.dialog = []
        for line in dialogue:
            self.dialog.append(line.rstrip())
        return self.dialog

    def get_npc_replicas(self, npc):
        """Возвращение всех локаций определенного npc"""
        return self.__dict_npc_loc[npc]

    @property
    def dict_npc_loc(self):
        return self.__dict_npc_loc

#
# check = ReadingLocations('proba.txt')
# print(check.dict_npc_loc)
# print(check.get_npc_replicas('a'))
