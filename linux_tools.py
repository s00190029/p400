import subprocess
from Xlib import X, display
import subprocess
import re
d = display.Display()
s = d.screen()
xroot = s.root
window_list = list()
windows = xroot.query_tree().children
blacklist = list()



def get_executable_path(processIn):
    result = subprocess.run("which " + processIn,
                            shell=True, capture_output=True)
    return result.stdout.decode().strip()


def get_window_list():
    for window in windows:
        text = window.get_wm_class()
    # print(text)
        window_list.append(text)
    return window_list

def format_list(listIn):
    # use ast.literal_eval() to convert the string to a list of tuples
    tuples_list = tuple(listIn)

    # use list comprehension to extract the second element of each tuple
    result = [x[0] for x in tuples_list if x is not None]

    # use ','.join() to join the list of strings into one string
    #result = ','.join(result)

    with open("blacklist.txt", "r") as blacklist_file:
        window_set = set(result)
        window_set.difference_update(blacklist_file)

    return window_set

def apply_blacklist(setIn):
    # Read the blacklist from the file
    with open("blacklist.txt", "r") as file:
        blacklist = file.read().splitlines()

    # Compile the blacklist into a set of regular expressions
    blacklist = {re.compile(item) for item in blacklist}

    # Create a new set containing only items that don't match the blacklist
    differenced_set = {x for x in setIn if not any(pattern.match(x) for pattern in blacklist)}
    

    return differenced_set
    


def produce_final_set():
    window_list_active = get_window_list()
    lowercase_list_active = [(x[0], x[1].lower()) if x is not None else None for x in window_list_active]
    window_set_active = set(lowercase_list_active)
    window_set_active = format_list(window_set_active)
    lowercase_set_active = {item.lower() for item in window_set_active}
    
    lowercase_set_active.discard('')

    #remove more blacklisted items
    """
    for p in patternlist:
        lowercase_set_active = {x for x in lowercase_set_active if not p.match(x)}
    """ 
    setOut = apply_blacklist(lowercase_set_active)
    return setOut

def clean_window(window_name_in):
    ref = ["wmctrl", "-r"]
    command_list_fullscreen = ref.copy(); command_list_fullscreen.extend([window_name_in, "-b", "remove,fullscreen"])
    command_list_vert = ref.copy(); command_list_vert.extend([window_name_in, "-b", "remove,maximized_vert"])
    command_list_horz = ref.copy(); command_list_horz.extend([window_name_in, "-b", "remove,maximized_horz"])
    command_list_size = ref.copy(); command_list_size.extend([window_name_in, "-e", "0,900,0,1280,720"])
    command_list = [command_list_fullscreen, command_list_horz, command_list_vert,command_list_size]
    
    for command in command_list:
        subprocess.run(command)

def get_exec_dir(nameIn):
    output = subprocess.check_output(["which", nameIn]).decode().strip()
    return output