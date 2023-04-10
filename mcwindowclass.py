from pywinauto import Application
import subprocess
import pygetwindow as gw

class MicrosoftWindow:
    def __init__(self, name, x_coord, y_coord, x_size, y_size, path):
        self.name = name
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.x_size = x_size
        self.y_size = y_size
        self.path = path

    def move(self):
        window = gw.getWindowsWithTitle(self.name)[0]
        window.moveTo(self.x_coord, self.y_coord)
        window.resizeTo(self.x_size, self.y_size)

    def execute(self):
        subprocess.Popen(self.path)

    def execute_safe(self):
        if not gw.getWindowsWithTitle(self.name):
            subprocess.Popen(self.path)

    def to_json(self):
        return {
            'name': self.name,
            'x_coord': self.x_coord,
            'y_coord': self.y_coord,
            'x_size': self.x_size,
            'y_size': self.y_size,
            'path': self.path
        }

    @classmethod
    def from_json(cls, data):
        return cls(
            name=data['name'],
            x_coord=data['x_coord'],
            y_coord=data['y_coord'],
            x_size=data['x_size'],
            y_size=data['y_size'],
            path=data['path']
        )