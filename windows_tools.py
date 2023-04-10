import json
import pygetwindow as gw
import win32gui
import win32con
import win32process
import psutil
import subprocess
from mcwindowclass import MicrosoftWindow
from mcwstack import MicrosoftWindowStack

def is_window_visible(hwnd):
    return win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd)

def get_process_path(hwnd):
    _, pid = win32process.GetWindowThreadProcessId(hwnd)
    process = psutil.Process(pid)
    return process.exe()

def get_open_files(pid):
    handle_path = r'C:\SysinternalsSuite\handle.exe'
    open_files = []

    try:
        # Run handle.exe and get the output
        result = subprocess.run([handle_path, '-p', str(pid), '-accepteula'], capture_output=True, text=True, check=True)
        output_lines = result.stdout.splitlines()

        # Parse the output to find open files
        for line in output_lines:
            if "File" in line:
                file_path = line.split()[-1]
                open_files.append(file_path)
    except subprocess.CalledProcessError as e:
        print(f"Error running handle.exe: {e}")

    return open_files

def get_open_windows():
    open_windows = []

    for window in gw.getAllWindows():
        hwnd = window._hWnd
        if is_window_visible(hwnd):
            title = window.title
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            #open_files = get_open_files(pid)

            window_details = {
                'title': title,
                'left': window.left,
                'top': window.top,
                'width': window.width,
                'height': window.height,
                'executable_path': get_process_path(hwnd),
                #'open_files': open_files,
            }
            currentWindow = MicrosoftWindow(window_details['title'],window_details['left'],window_details['top'],window_details['width'],window_details['height'],window_details['executable_path'])
            #print(window_details['title'])
            open_windows.append(currentWindow)

    return open_windows


def getCurrentMicrosoftStack():
    currentStack = MicrosoftWindowStack("tempStack", get_open_windows())


