import subprocess
import linux_tools
import asyncio
import json
import multiprocessing

wmRef = ['wmctrl', '-r']

class LinuxWindow:
    def __init__(self,name,x_coord,y_coord,x_size,y_size):
        self.name = name
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.x_size = x_size
        self.y_size = y_size
        self.path = linux_tools.getExecDir(name)
        self.stringCoords = "'0,{},{},{},{}'".format(str(self.x_coord),str(self.y_coord),str(self.x_size),str(self.y_size))


    def move(self):
        # hardcoded values. Change to dynamic
        subprocess.run(wmRef.copy().extend(['-e', '0,0,0,500,500']))

    def execute(self):
        subprocess.Popen(self.path) 

    def executeSafe(self):
        if linux_tools.isProcessRunning(self.name) == False:
            subprocess.Popen(self.path) 
    """
    def saveSelf(self):
        with open(self.name, 'w') as file:
            json.dump({
                'name': self.name,
            }, file, indent=4)
    """
    def to_json(self):
        return {
            'name': self.name,
            'x_coord': self.x_coord,
            'y_coord': self.y_coord,
            'x_size': self.x_size,
            'y_size': self.y_size,
            'path': self.path,
            'stringCoords': self.stringCoords
        }
    
    @classmethod
    def from_json(cls, data):
        return cls(
            name=data['name'],
            x_coord=data['x_coord'],
            y_coord=data['y_coord'],
            x_size=data['x_size'],
            y_size=data['y_size']
        )

class LinuxStack:
    def __init__(self,name, process_list = []):
        self.name = name
        self.process_list = process_list

    def launch(self):
        for p in self.process_list:
                p.executeSafe()
            
    def to_json(self):
        return {
            'name': self.name,
            'process_list': [window.to_json() for window in self.process_list]
        }

    @classmethod
    def from_json(cls, data):
        process_list = [LinuxWindow.from_json(process_data) for process_data in data['process_list']]
        return cls(name=data['name'], process_list=process_list)
    
