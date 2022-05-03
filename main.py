import tkinter as tk
from tkinter import CENTER, LEFT, ttk
from tkinter import messagebox
from pymongo import MongoClient, collection
import ui

import sys, os

dir_path = os.path.dirname(os.path.realpath(__file__))
api_path = ""
for dir in os.listdir(dir_path):
    dir = os.path.join(dir_path, dir)
    if "api" in dir:
        print(dir)
        api_path = dir
        break
sys.path.insert(1, api_path)
print(sys.path)


root = ui.MainUI()
root.title("Advanced Programming")

# closing function
def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()


# an event to close window
def close_win(e, root: tk.Tk):
    root.destroy()


def hide_button(widget):
    # This will remove the widget from toplevel
    widget.pack_forget()

# main tinker window layout
def create_main_window(window_width=1200, window_height=600):
    # create tinker window with fixed size as in widthxheight±x±y
    window_width = 1200
    window_height = 600

    # get the screen dimension -> from our desktop
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # find the center point of our desktop
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)

    # set the position of the window to the center of the screen
    root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")


# start the ui loop
def start_window():
    # fix blur in ui
    try:
        from ctypes import windll

        windll.shcore.SetProcessDpiAwareness(1)
    finally:
        root.protocol("WM_DELETE_WINDOW", on_closing)
        root.mainloop()


# function to create main window
def create_button_frame(container):

    frame = ttk.Frame(container)

    frame.columnconfigure(0, weight=1)

    # create a button to show airport data
    all_data = ttk.Button(
        root, text="Show All Airport Data", command=query_collection_result
    )
    all_data.grid(column=0, row=1, sticky=tk.EW, padx=1, pady=1)

    # frequency data button
    freq_data = ttk.Button(
        root, text="show Frequency Data", command=query_collection_result
    )
    freq_data.grid(column=0, row=2, sticky=tk.EW, padx=1, pady=1)

    # runway data button
    runway_data = ttk.Button(
        root, text="Show Runway Data", command=query_collection_result
    )
    runway_data.grid(column=0, row=3, sticky=tk.EW, padx=1, pady=1)

    # uk data
    uk_airport_data = ttk.Button(
        root, text="Show UK Airport Frequency Data", command=query_collection_result
    )
    uk_airport_data.grid(column=0, row=4, sticky=tk.EW, padx=1, pady=1)

    # create button to implement destroy()
    quit_button = ttk.Button(root, text="Quit", command=on_closing)
    quit_button.grid(column=0, row=5, sticky=tk.EW, padx=1, pady=1)

    for widget in frame.winfo_children():
        widget.grid(padx=0, pady=3)

    return frame


if __name__ == "__main__":

    create_main_window()

    # createa the container grid
    root.columnconfigure(0, weight=3)
    root.columnconfigure(1, weight=6)
    root.columnconfigure(2, weight=6)

    # create event binding, press esc to exit
    root.bind("<Escape>", lambda e: close_win(e, root=root))

    start_window()

