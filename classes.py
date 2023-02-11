import subprocess
import linux_tools
import asyncio
import multiprocessing

wmRef = ['wmctrl', '-r']

class LinuxWindow:
    def __init__(self,name,x_coord,y_coord,x_size,y_size):
        self.name = name
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.x_size = x_size
        self.y_size = y_size
        self.path = linux_tools.get_exec_dir(name)
        self.stringCoords = "'0,{},{},{},{}'".format(str(self.x_coord),str(self.y_coord),str(self.x_size),str(self.y_size))


    def move(self):
        subprocess.run(wmRef.copy().extend(['-e', '0,0,0,500,500']))

    def execute(self):
        subprocess.Popen(self.path) 

class LinuxStack:
    def __init__(self,name, process_list = []):
        self.name = name
        self.process_list = process_list

    def launch(self):
        for p in self.process_list:
            p.execute()