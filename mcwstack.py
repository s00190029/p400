from mcwindowclass import MicrosoftWindow

class MicrosoftWindowStack:
    def __init__(self, name, window_list=[]):
        self.name = name
        self.window_list = window_list

    def launch(self):
        for window in self.window_list:
            window.execute_safe()

    def to_json(self):
        return {
            'name': self.name,
            'window_list': [window.to_json() for window in self.window_list]
        }

    @classmethod
    def from_json(cls, data):
        window_list = [MicrosoftWindow.from_json(window_data) for window_data in data['window_list']]
        return cls(name=data['name'], window_list=window_list)
