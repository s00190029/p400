import tkinter as tk
import asyncio
import platform
import ast
import re
import subprocess
import os
import json

# Colour Variables
bg_colour = "#2f3136"
colour_white = "#ffffff"
activebackground_colour = "#434c5e"


async def wgui() -> None:

    def button1_callback():
        # Clear text box so it doesn't get cluttered
        clear_text(text_box)

        # Setup a temporary process stack class and fill it with the currently running processes
        

        # Write into the texbox to show user the process list
        

        # Save the temp stack to disk for later
        

        # Update stack buttons
        populateStackButtons()

    def button2_callback():
        print("Button 2 clicked")

    def button3_callback():
        clear_text(text_box)
        text_box.insert("1.0","test insert")

    def clear_text(box_name):
        box_name.delete("1.0", "end")

    # Create the main window
    root = tk.Tk()
    root.title("Launcher Tool")

    # Set the window size
    root.geometry("1280x720")

    # Set the background color
    root["bg"] = "black"

    # Create the 3 buttons
    button1 = tk.Button(root, text="Capture", command=button1_callback, bg=bg_colour,
                        fg=colour_white, activebackground=activebackground_colour, activeforeground=colour_white)
    button2 = tk.Button(root, text="Launch", command=button2_callback, bg=bg_colour,
                        fg=colour_white, activebackground=activebackground_colour, activeforeground=colour_white)
    button3 = tk.Button(root, text="Button 3", command=button3_callback, bg=bg_colour,
                        fg=colour_white, activebackground=activebackground_colour, activeforeground=colour_white)

    # Place the buttons in a horizontal layout using the grid layout manager
    button1.grid(row=0, column=0, sticky="ew")
    button2.grid(row=0, column=1, sticky="ew")
    button3.grid(row=0, column=2, sticky="ew")

    # Set the row and column weights to 1 to make the layout responsive to window resizing
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)
    root.columnconfigure(2, weight=1)

    # Create the text box
    text_box = tk.Text(root, bg=bg_colour, fg=colour_white, insertbackground=colour_white, highlightbackground=bg_colour,
                       highlightcolor=colour_white, selectbackground=bg_colour, selectforeground=colour_white)
    text_box.grid(row=1, column=0, columnspan=3, sticky="ew")


    def create_button(json_file):
        with open(json_file, "r") as f:
            data = json.load(f)
            #tempStack = LinuxStack.from_json(data)
            button_text = os.path.splitext(json_file)[0]
            button = tk.Button(root, text=button_text, bg=bg_colour, fg=colour_white,
                               activebackground=activebackground_colour, activeforeground=colour_white, command=lambda: tempStack.launch())
            return button

    def populateStackButtons():

        # Get the list of JSON files in the current directory
        # Will need to update later for a dedicated json folder both here and in class
        json_files = [f for f in os.listdir(".") if f.endswith(".json")]
        buttons = []
        
        # Create a button for each JSON file
        colNum = 0
        for i, json_file in enumerate(json_files):
            button = create_button(json_file)
            #rowAddition = linux.calcGUIRows(buttons)
            button.grid(row=2+0, column=colNum, sticky="ew")
            colNum += 1
            if colNum >= 3:
                colNum = 0
            buttons.append(button)
        buttons.sort

    populateStackButtons()

    # Run the main loop
    root.mainloop()


