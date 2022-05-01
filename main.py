import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter.tix import Tk
import ui

# closing function
def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()


# an event to close window
def close_win(e, root: tk.Tk):
    root.destroy()


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
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)

    # set the position of the window to the center of the screen
    root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

    # createa the container grid
    root.columnconfigure(0, weight=3)
    root.columnconfigure(1, weight=6)

    # place a label on the root window
    message = tk.Label(root, text="Airport Data Analysis", font=("Times New Roman", 18))
    message.grid(column=1, row=0, sticky=tk.EW, padx=5, pady=5)

    # create a button to show airport data
    all_data = ttk.Button(root, text="Show All Airport Data", command=ui.button_clicked)
    all_data.grid(column=0, row=1, sticky=tk.EW, padx=1, pady=1)

    # frequency data button
    freq_data = ttk.Button(root, text="show Frequency Data", command=ui.button_clicked)
    freq_data.grid(column=0, row=2, sticky=tk.EW, padx=1, pady=1)

    # runway data button
    runway_data = ttk.Button(root, text="Show Runway Data", command=ui.button_clicked)
    runway_data.grid(column=0, row=3, sticky=tk.EW, padx=1, pady=1)

    # uk data
    uk_airport_data = ttk.Button(
        root, text="Show UK Airport Frequency Data", command=ui.button_clicked
    )
    uk_airport_data.grid(column=0, row=4, sticky=tk.EW, padx=1, pady=1)

    # create button to implement destroy()
    quit_button = ttk.Button(root, text="Quit", command=on_closing)
    quit_button.grid(column=0, row=5, sticky=tk.EW, padx=1, pady=1)

    # create event binding, press esc to exit
    root.bind("<Escape>", lambda e: close_win(e, root=root))

    # fix blur in ui
    try:
        from ctypes import windll

        windll.shcore.SetProcessDpiAwareness(1)
    finally:
        root.protocol("WM_DELETE_WINDOW", on_closing)
        root.mainloop()

    root.mainloop()
