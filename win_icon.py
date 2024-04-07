import os
import ctypes
import tkinter as tk
from tkinter import ttk

window = tk.Tk()
window.title("Character Viewer")
window.geometry("1000x700")

# Set the App ID for Windows taskbar
app_id = "comp-500-character-viewer"
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)

# Get directory path
abs_path = os.path.abspath(__file__)
dir_name = os.path.dirname(abs_path)

# Set window icon
icon_path = os.path.join(dir_name, "image.ico")
window.iconbitmap(icon_path)

# Set character images
img_path = os.path.join(dir_name, 'spongebob.png')
img = tk.PhotoImage(file=img_path)

# Event handler method for the combobox
def option_selected(event):
    character_list = ("spongebob.png", "squidward.png")
    character_index = com_box.current()
    img['file'] = os.path.join(dir_name, character_list[character_index])

# Frame configuration
window.rowconfigure(0, weight=1)
window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=1)

frame1 = ttk.Frame(window)
frame1.grid(row=0, column=0)

# Combobox
character_list = ("SpongeBob", "Squidward")
com_box = ttk.Combobox(frame1, values=character_list)
com_box.bind("<<ComboboxSelected>>", option_selected)
com_box.grid(row=0, column=0)

frame2 = ttk.Frame(window)
frame2.grid(row=0, column=1)

# Label for displaying the image
label2 = ttk.Label(frame2, text="Character Image", image=img, anchor="center")
label2.grid(row=0, column=0)

window.mainloop()
