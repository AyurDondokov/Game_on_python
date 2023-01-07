from abc import ABC, abstractmethod


class Script(ABC):
    """Патерн команда для скриптов"""

    def __init__(self, receiver) -> None:
        self._reseiver = receiver

    @abstractmethod
    def execute(self):
        """Должен запускать метод конкретного обьекта"""
        pass


class TestScript(Script):
    def execute(self):
        print("Script activated")


class StartBattleScript(Script):
    def __init__(self, receiver, battle_index):
        super().__init__(receiver)
        self._battle_index = battle_index

    def execute(self):
        """Запускает бой"""
        self._reseiver.start(self._battle_index)


class SwitchDialog(Script):
    def execute(self):
        """Включает следующую реплику у NPC"""
        self._reseiver.nextDalog()


class ActivatePortalScript(Script):
    def execute(self):

        self._reseiver.activate()

    @property
    def receiver(self):
        return None

    @receiver.setter
    def receiver(self, receiver):
        self._reseiver = receiver
        print(self._reseiver)
