import subprocess
import linux_tools
import asyncio

wmRef = ['wmctrl', '-r']

class LinuxWindow:
    def __init__(self,name,x_coords,y_coords,x_size,y_size):
        self.name = name
        self.x_coords = x_coords
        self.y_coords = y_coords
        self.x_size = x_size;
        self.y_size = y_size
        self.path = linux_tools.get_exec_dir(name)


    def move(self):
        subprocess.run(wmRef.copy().extend(['-e', '0,0,0,500,500']))

    async def execute(self):
        subprocess.run("{} &".format(self.path))   

    """
    import asyncio

class LinuxWindow:
    async def execute(self):
        print("Executing...")
        process = await asyncio.create_subprocess_exec(*self.path)
        await process.wait()
        print("Execution finished.")

    """

        
    