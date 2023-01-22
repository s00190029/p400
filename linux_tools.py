import subprocess

class linux_tools:
    
    def get_executable_path(processIn):
        result = subprocess.run("which " + processIn, shell=True, capture_output=True)
        return result.stdout.decode().strip()
