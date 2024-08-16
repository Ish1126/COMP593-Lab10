from tkinter import *
from tkinter import ttk
import os
import poke_api
import image_lib
import inspect
from PIL import Image, ImageTk  # Import the necessary modules from PIL

# Global variable to store the current image path
current_image_path = None

# Get the script and images directory
script_name = inspect.getframeinfo(inspect.currentframe()).filename
script_dir = os.path.dirname(os.path.abspath(script_name))
images_dir = os.path.join(script_dir, 'images')

# Create the images directory if it does not exist
if not os.path.exists(images_dir):
    os.makedirs(images_dir)

# Create the main window
root = Tk()
root.title("Pokemon Viewer")
root.geometry('600x600')
root.minsize(500, 600)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Create frames
frm = ttk.Frame(root)
frm.columnconfigure(0, weight=1)
frm.rowconfigure(0, weight=1)
frm.grid(sticky=NSEW)

# Set default image path and load image using Pillow
default_image_path = os.path.join(images_dir, 'poke_ball.ico')
if not os.path.exists(default_image_path):
    raise FileNotFoundError(f"Default image file not found at {default_image_path}")

# Open the image using Pillow and convert it to a PhotoImage that Tkinter can use
image = Image.open(default_image_path)
photo = ImageTk.PhotoImage(image)

# Display the image in the label
lbl_image = ttk.Label(frm, image=photo)
lbl_image.grid(row=0, column=0, padx=10, pady=10)

# Create dropdown (Combobox) to select Pokémon
pokemon_names = poke_api.get_pokemon_names()
cbox_poke_sel = ttk.Combobox(frm, values=pokemon_names, state='readonly')
cbox_poke_sel.grid(row=1, column=0, padx=10, pady=10)
cbox_poke_sel.set('Select a Pokémon')

# Create button to set desktop background
btn_set_desktop = ttk.Button(frm, text="Set as Desktop Background", command=lambda: handle_set_desktop())
btn_set_desktop.grid(row=2, column=0, padx=10, pady=10)
btn_set_desktop['state'] = 'disabled'  # Disable button by default

# Event handler function for Pokémon selection
def handle_poke_sel(event):
    global current_image_path  # Use the global variable to store the image path
    pokemon_name = cbox_poke_sel.get()
    image_path = poke_api.download_pokemon_artwork(pokemon_name, images_dir)
    if image_path:
        image = Image.open(image_path)
        photo = ImageTk.PhotoImage(image)
        lbl_image.config(image=photo)
        lbl_image.image = photo  # Prevent garbage collection of the image
        current_image_path = image_path  # Store the image path
        btn_set_desktop['state'] = 'normal'  # Enable the button

cbox_poke_sel.bind('<<ComboboxSelected>>', handle_poke_sel)

# Event handler function for setting desktop background
def handle_set_desktop():
    if current_image_path:  # Ensure there's an image path stored
        image_lib.set_desktop_background_image(current_image_path)

root.mainloop()
