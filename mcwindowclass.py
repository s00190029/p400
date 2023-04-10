import subprocess
from pywinauto import Application

class MicrosoftWindow:
    def __init__(self, name, x_coord, y_coord, x_size, y_size, pathIn):
        self.name = name
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.x_size = x_size
        self.y_size = y_size
        self.path = pathIn

    @classmethod
    def execute(self) -> None:
        subprocess.Popen(self.path)

    @classmethod
    def move(self) -> None:
        app_name = self.path
        window_title = "Untitled - Notepad"

        app = Application(backend="uia").connect(path=app_name)
        window = app.window(title_re=window_title)
