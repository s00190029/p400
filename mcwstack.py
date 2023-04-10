import mcwindowclass

class MicrosoftWindowStack:
    def __init__(self, name, windowList, ):
        self.name = name
        self.windowList = windowList

    @classmethod
    def execute(self) -> None:
        for window in self.windowList:
            window.execute()
