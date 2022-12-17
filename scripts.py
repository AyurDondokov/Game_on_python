class Script:
    def __init__(self, func) -> None:
        self.func = func

    def run(self):
        self.func()
