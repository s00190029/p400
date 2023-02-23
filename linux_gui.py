import tkinter as tk
import asyncio
import platform
import ast
import re
import linux_tools as linux
from classes import LinuxStack
from classes import LinuxWindow
import gen_tools
import subprocess

# Colour Variables
bg_colour = "#2f3136"
colour_white = "#ffffff"
activebackground_colour = "#434c5e"

async def main() -> None:
    
    def button1_callback():
        clear_text(text_box)        
        print("Button 1 clicked")
        global tempStack
        tempList = gen_tools.produceFinalProcessList()
        print("Templist is of type {}".format(type(tempList)))
        tempStack = LinuxStack("tempStack",tempList)
        for n in tempList:
            text_box.insert("1.0"," {}, ".format(n.name))
        #f = open("testFile.txt", "w")
        #f.write(tempStack)
        
    def button2_callback():
        print("Button 2 clicked")
        tempStack.launch()

    def button3_callback():
        clear_text(text_box)
        final_window_set=linux.produceCurrentWindowSet()
        for item in final_window_set:
            print(linux.getExecutablePath(item))

        print(final_window_set)
        text_box.insert("1.0",final_window_set)

    # Create the main window
    root = tk.Tk()
    root.title("Launcher Tool")

    # Set the window size (16:9 aspect ratio)
    root.geometry("1280x720")

    # Set the background color to a dark color
    root["bg"] = "black"

    # Create the 3 buttons
    button1 = tk.Button(root, text="Capture", command=button1_callback, bg=bg_colour, fg=colour_white, activebackground=activebackground_colour, activeforeground=colour_white)
    button2 = tk.Button(root, text="Launch", command=button2_callback, bg=bg_colour, fg=colour_white, activebackground=activebackground_colour, activeforeground=colour_white)
    button3 = tk.Button(root, text="Button 3", command=button3_callback, bg=bg_colour, fg=colour_white, activebackground=activebackground_colour, activeforeground=colour_white)

    # Place the buttons in a horizontal layout using the grid layout manager
    button1.grid(row=0, column=0, sticky="ew")
    button2.grid(row=0, column=1, sticky="ew")
    button3.grid(row=0, column=2, sticky="ew")

    # Set the row and column weights to 1 to make the layout responsive to window resizing
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)
    root.columnconfigure(2, weight=1)

    # Create the text box
    text_box = tk.Text(root, bg=bg_colour, fg=colour_white, insertbackground=colour_white, highlightbackground=bg_colour, highlightcolor=colour_white, selectbackground=bg_colour, selectforeground=colour_white)
    text_box.grid(row=1, column=0, columnspan=3, sticky="ew")
    def clear_text(box_name):
        box_name.delete("1.0", "end")

    # Run the main loop
    root.mainloop()

asyncio.run(main())