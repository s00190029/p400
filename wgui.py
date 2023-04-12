import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
import windows_tools
import globalTools
import mcwstack
import os
import json
import asyncio

class LauncherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Launcher Tool")
        self.root.geometry("1280x720")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self.root)
        main_frame.grid(row=0, column=0, sticky="nsew")

        # create buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=0, column=0, sticky="ew", pady=(10, 5), padx=(20, 20))
        button_frame.columnconfigure(0, weight=1)

        button1 = ttk.Button(button_frame, text="Capture 📸", command=lambda: button1_callback(self))
        button1.grid(row=0, column=0, padx=(0, 5), sticky="ew")

        # create information label
        self.info_label = tk.Label(main_frame, wraplength=1200, anchor="w", justify="left")
        self.info_label.grid(row=1, column=0, sticky="nsew", pady=(5, 10), padx=(20, 20))

        # Set uniform option for the main_frame grid cells
        main_frame.columnconfigure(0, weight=1, uniform="main")

        # call the function to populate the stack buttons
        self.populate_stack_buttons()

    def populate_stack_buttons(self):
        json_files = [f for f in os.listdir(".") if f.endswith(".json")]

        button_frame = ttk.Frame(self.root)
        button_frame.grid(row=2, column=0, sticky="ew", pady=(5, 10), padx=(20, 20))

        button_width = 20

        for i, json_file in enumerate(json_files):
            button = self.create_button(button_frame, json_file, button_width)
            button.grid(row=i // 3, column=i % 3, pady=(0, 5), padx=(5, 5), sticky="ew")

            # uniform option for the button grid cell
            button_frame.columnconfigure(i % 3, weight=1, uniform="button")

    def create_button(self, button_frame, json_file, button_width):
        with open(json_file, "r") as f:
            data = json.load(f)
            tempStack = mcwstack.MicrosoftWindowStack.from_json(data)
            button_text = os.path.splitext(json_file)[0]
            button = ttk.Button(button_frame, text=button_text, command=lambda: tempStack.launch(), width=button_width)
            return button

def button1_callback(app_instance):
    app_instance.info_label.config(text="")  # Clear the label text
    global tempStack
    tempStack = windows_tools.getCurrentMicrosoftStack()

    # Write into the label to show user the process list
    process_list_text = ""
    for twindow in tempStack.window_list:
        process_list_text += " {} {}, ".format(twindow.name, twindow.path)
    
    app_instance.info_label.config(text=process_list_text)

    # save the temp stack to disk for later
    globalTools.writeStackToJson(tempStack)

    # call the populate_stack_buttons method on the app_instance
    app_instance.populate_stack_buttons()

async def main():
    root = ThemedTk(theme="arc")  # You can choose another theme if you prefer
    app = LauncherApp(root)
    root.mainloop()

if __name__ == "__main__":
    asyncio.run(main())
