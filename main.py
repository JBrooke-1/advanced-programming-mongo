import tkinter as tk
from tkinter import ttk
import ui
# import console

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Advanced Programming")

    # create tinker window with fixed size as in widthxheight±x±y
    window_width = 800
    window_height = 600

    # get the screen dimension -> from our desktop
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # find the center point of our desktop
    center_x = int(screen_width/2 - window_width / 2)
    center_y = int(screen_height/2 - window_height / 2)

    # set the position of the window to the center of the screen
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

    # place a label on the root window
    message = tk.Label(root, text="Airport Data Analysis")
    message.pack()

    # create a button and dummy function
    button = ttk.Button(root, text='Show All Data', command=ui.button_clicked)
    button.pack()



    # fix blur in ui
    try:
        from ctypes import windll

        windll.shcore.SetProcessDpiAwareness(1)
    finally:
        root.mainloop()
