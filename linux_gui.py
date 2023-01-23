import tkinter as tk
import asyncio
import platform
import ast
import re
import linux_tools as linux
from window_linux_class import LinuxWindow as lprocess
import subprocess


final_window_set=linux.produce_final_set()
print(final_window_set)


def button1_callback():
    # Placeholder method for button 1
    print("Button 1 clicked")
    kateProgram = lprocess("kate", 1, 2, 3, 4)
    asyncio.run(kateProgram.execute())


def button2_callback():
    linux.clean_window("kate")
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
button1 = tk.Button(root, text="Button 1", command=lambda: asyncio.get_event_loop().run_in_executor(None,button1_callback), bg="#2f3136", fg="#ffffff", activebackground="#434c5e", activeforeground="#ffffff")
button1.pack()
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

#exec_list.append(get_exec_dir("firefox"))
#exec_list.append(get_exec_dir("kate"))

#text_box.insert("1.0", "placeholder!!!")

# Place the text box below the buttons
text_box.grid(row=1, column=0, columnspan=3, sticky="ew")


# Testing area

for item in final_window_set:
    print(linux.get_executable_path(item))



# Run the main loop
root.mainloop()

