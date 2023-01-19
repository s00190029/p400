import tkinter as tk
from Xlib import X, display
import subprocess


d = display.Display()
s = d.screen()
xroot = s.root
window_list = set()
windows = xroot.query_tree().children

for window in windows:
    if window.get_attributes().map_state == X.IsViewable:
        text = window.get_wm_name() or window.get_wm_class()
       # print(text)
        window_list.add(text)

window_list.discard('None')    
window_list.discard(None)    


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
text_box.insert("1.0",window_list)

exec_list = list()
def get_exec_dir(nameIn):
    output = subprocess.check_output(["which", nameIn]).decode().strip()
    return output


exec_list.append(get_exec_dir("firefox"))
exec_list.append(get_exec_dir("kate"))



text_box.insert("1.0", exec_list)

# Place the text box below the buttons
text_box.grid(row=1, column=0, columnspan=3, sticky="ew")

print(window_list)

# Run the main loop
root.mainloop()
