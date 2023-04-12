import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
import windows_tools
import globalTools
import mcwstack
import os
import json
import asyncio
import time
from tkinter import simpledialog


class LauncherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Launcher Tool")
        self.root.geometry("1280x720")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, style="main_frame.TFrame")
        main_frame.grid(row=0, column=0, sticky="nsew")

        # create buttons
        button_frame = ttk.Frame(main_frame, style="button_frame.TFrame")
        button_frame.grid(row=0, column=0, sticky="ew", pady=(10, 5), padx=(20, 20))
        button_frame.columnconfigure(0, weight=1)

        button1 = ttk.Button(button_frame, text="Capture 📸", command=lambda: button1_callback(self))
        button1.grid(row=0, column=0, padx=(0, 5), sticky="ew")

        # Create the info_label
        self.info_label = ttk.Label(main_frame, text="", style="custom_label.TLabel")
        self.info_label.grid(row=2, column=0, sticky="ew", pady=(5, 5), padx=(20, 20))

        # Configure the main_frame to use the available space
        self.root.columnconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)

        # call the function to populate the stack buttons
        self.populate_stack_buttons()





    def populate_stack_buttons(self):
        json_files = [f for f in os.listdir(".") if f.endswith(".json")]

        button_frame = ttk.Frame(self.root)
        button_frame.grid(row=2, column=0, sticky="ew",
                          pady=(5, 10), padx=(20, 20))

        button_width = 20

        for i, json_file in enumerate(json_files):
            button = self.create_button(button_frame, json_file, button_width)
            button.grid(row=i // 3, column=i %
                        3, pady=(0, 5), padx=(5, 5), sticky="ew")

            # uniform option for the button grid cell
            button_frame.columnconfigure(i % 3, weight=1, uniform="button")

    # using button_frame and button_width as arguments
    def create_button(self, button_frame, json_file, button_width):
        with open(json_file, "r") as f:
            data = json.load(f)
            tempStack = mcwstack.MicrosoftWindowStack.from_json(data)
            button_text = os.path.splitext(json_file)[0]
            # using button_frame and set the width
            button = ttk.Button(
                button_frame, text=button_text, width=button_width)
            button.json_file = json_file  # store the json_file as a attribute of the button
            button.bind(
                "<Button-1>", lambda event: self.on_button_press(event, tempStack))
            button.bind("<ButtonRelease-1>",
                        lambda event: self.on_button_release(event, button))
            return button

    def show_rename_delete_dialog(self, button):
        def rename_workspace():
            new_name = simpledialog.askstring(
                "Rename workspace", "Enter new workspace name:")
            if new_name:
                os.rename(button.json_file, new_name + ".json")
                button.config(text=new_name)
                button.json_file = new_name + ".json"  # update
                self.root.focus()

        def delete_workspace():
            os.remove(button.json_file)
            button.destroy()
            dialog.destroy()
            self.root.focus()

        dialog = tk.Toplevel(self.root)
        dialog.title("Options")
        dialog.geometry("200x100")

        rename_button = ttk.Button(
            dialog, text="Rename", command=rename_workspace)
        rename_button.pack(fill="both", expand=True)

        delete_button = ttk.Button(
            dialog, text="Delete", command=delete_workspace)
        delete_button.pack(fill="both", expand=True)

    def on_button_press(self, event, tempStack):
        self.press_time = time.time()
        self.stack_to_launch = tempStack

    def on_button_release(self, event, button):
        release_time = time.time()
        if release_time - self.press_time > 0.5:  # experiment with timings based on user feedback
            self.show_rename_delete_dialog(button)
        else:
            self.stack_to_launch.launch()


def button1_callback(app_instance):
    # render the custom dialog and get the workspace name
    dialog = WorkspaceNameDialog(app_instance.root)
    app_instance.root.wait_window(dialog)
    workspace_name = dialog.workspace_name.get()

    if not workspace_name:  # if user doesn't enter a name, don't continue
        return

    app_instance.info_label.config(text="")
    global tempStack
    tempStack = windows_tools.getCurrentMicrosoftStack()

    # Write into the label to show user the process list
    process_list_text = ""
    for twindow in tempStack.window_list:
        process_list_text += " {} {}, ".format(twindow.name, twindow.path)

    app_instance.info_label.config(text=process_list_text)

    # save the temp stack to disk for later
    json_filename = "{}.json".format(workspace_name)
    globalTools.writeStackToJson(tempStack, json_filename)

    app_instance.populate_stack_buttons()

class WorkspaceNameDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Enter Workspace Name")
        self.geometry("300x100")

        self.workspace_name = tk.StringVar()

        style = ttk.Style(self)
        self.configure(bg=style.lookup("TFrame", "background"))

        label = ttk.Label(self, text="Workspace Name:", style="custom_label.TLabel")
        label.grid(row=0, column=0, padx=10, pady=10)

        entry = ttk.Entry(self, textvariable=self.workspace_name)
        entry.grid(row=0, column=1, padx=10, pady=10)

        ok_button = ttk.Button(self, text="OK", command=self.ok)
        ok_button.grid(row=1, column=0, columnspan=2, pady=10)

        entry.focus_set()

    def ok(self):
        self.destroy()


async def main():
    root = ThemedTk(theme="equilux")
    style = ttk.Style(root)
    style.configure("main_frame.TFrame", background=style.lookup("TFrame", "background"))
    style.configure("button_frame.TFrame", background=style.lookup("TFrame", "background"))

    # Custom style for the Label widget
    style.configure("custom_label.TLabel", background=style.lookup("TFrame", "background"), foreground=style.lookup("TLabel", "foreground"))

    # Set the root window background color
    root.configure(bg=style.lookup("TFrame", "background"))

    app = LauncherApp(root)
    root.mainloop()




if __name__ == "__main__":
    asyncio.run(main())
