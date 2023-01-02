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


class StartBatlleScript(Script):

    def execute(self):
        """Запускает бой"""
        self._reseiver.start()


class SwitchDialog(Script):
    def execute(self):
        """Включает следующую реплику у NPC"""
        self._reseiver.nextDalog()
