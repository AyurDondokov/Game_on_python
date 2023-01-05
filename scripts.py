from abc import ABC, abstractmethod


class Script(ABC):
    """Патерн команда для скриптов"""

    def __init__(self, receiver) -> None:
        self.reseiver = receiver

    @abstractmethod
    def execute(self):
        """Должен запускать метод конкретного обьекта"""
        pass


class TestScript(Script):
    def execute(self):
        print("Script activated")


class StartBattleScript(Script):

    def execute(self):
        """Запускает бой"""
        self.reseiver.start()


class SwitchDialog(Script):
    def execute(self):
        """Включает следующую реплику у NPC"""
        self.reseiver.nextDalog()
