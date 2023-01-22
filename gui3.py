import tkinter as tk
import platform
import ast
from Xlib import X, display
import subprocess
import re
import linux_tools as linux


d = display.Display()
s = d.screen()
xroot = s.root
window_list = list()
windows = xroot.query_tree().children
blacklist = list()
pattern1 = re.compile("^gsd.*"); pattern2 = re.compile("^xdg.*"); pattern3 = re.compile("^org.*"); pattern4 = re.compile("^evolution.*")
pattern5 = re.compile("^lol.*"); pattern6 = re.compile("^ibus.*")
patternlist = (pattern1,pattern2,pattern3,pattern4,pattern5,pattern6)

def get_window_list():
    for window in windows:
            text =  window.get_wm_class()
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

final_window_set=produce_final_set()
print(final_window_set)


def button1_callback():
    # Placeholder method for button 1
    print("Button 1 clicked")

def button2_callback():
    # Placeholder method for button 2
    print("Button 2 clicked")

def button3_callback():
    # Placeholder method for button 3
    print("Button 3 clicked")

# Create the main window
root = tk.Tk()
root.title("Launcher Tool")

# Set the window size to 800x450 (16:9 aspect ratio)
root.geometry("800x450")

# Set the background color to a dark color
#root.configure(background="#36393f")
root["bg"] = "#36393f"

# Set the foreground (text) color to a light color
#root.configure(foreground="#ffffff")
root["bg"] = "black"


# Create the 3 buttons
button1 = tk.Button(root, text="Button 1", command=button1_callback, bg="#2f3136", fg="#ffffff", activebackground="#434c5e", activeforeground="#ffffff")
button2 = tk.Button(root, text="Button 2", command=button2_callback, bg="#2f3136", fg="#ffffff", activebackground="#434c5e", activeforeground="#ffffff")
button3 = tk.Button(root, text="Button 3", command=button3_callback, bg="#2f3136", fg="#ffffff", activebackground="#434c5e", activeforeground="#ffffff")

# Place the buttons in a horizontal layout using the grid layout manager
button1.grid(row=0, column=0, sticky="ew")
button2.grid(row=0, column=1, sticky="ew")
button3.grid(row=0, column=2, sticky="ew")

# Set the row and column weights to 1 to make the layout responsive to window resizing
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)

# Create the text box
text_box = tk.Text(root, bg="#2f3136", fg="#ffffff", insertbackground="#ffffff", highlightbackground="#2f3136", highlightcolor="#ffffff", selectbackground="#2f3136", selectforeground="#ffffff")

# Add placeholder text to the text box
def clear_text(box_name):
    box_name.delete("1.0", "end")

text_box.insert("1.0", "Placeholder text")
text_box.insert("1.0","lol")
text_box.insert("1.0","lol2")
clear_text(text_box)

# Print out current windows 
text_box.insert("1.0",final_window_set)


exec_list = list()
def get_exec_dir(nameIn):
    output = subprocess.check_output(["which", nameIn]).decode().strip()
    return output
#exec_list.append(get_exec_dir("firefox"))
#exec_list.append(get_exec_dir("kate"))

#text_box.insert("1.0", "placeholder!!!")

# Place the text box below the buttons
text_box.grid(row=1, column=0, columnspan=3, sticky="ew")

def clean_window(window_name_in):
    ref = ["wmctrl", "-r"]
    command_list_fullscreen = ref.copy(); command_list_fullscreen.extend([window_name_in, "-b", "remove,fullscreen"])
    command_list_vert = ref.copy(); command_list_vert.extend([window_name_in, "-b", "remove,maximized_vert"])
    command_list_horz = ref.copy(); command_list_horz.extend([window_name_in, "-b", "remove,maximized_horz"])
    command_list_size = ref.copy(); command_list_size.extend([window_name_in, "-e", "0,900,0,1280,720"])
    command_list = [command_list_fullscreen, command_list_horz, command_list_vert,command_list_size]
    
    for command in command_list:
        subprocess.run(command)
    
clean_window("super")

for item in final_window_set:
    print(linux.linux_tools.get_executable_path(item))

# Run the main loop
root.mainloop()
