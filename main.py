import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter.tix import Tk
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
    message = tk.Label(root, text="Airport Data Analysis", font=('Times New Roman', 18))
    message.pack()

    # create a button to show airport data
    ttk.Button(root, text='Show All Airport Data', command=ui.button_clicked).pack()
    ttk.Button(root, text='show Frequency Data', command=ui.button_clicked).pack()
    ttk.Button(root, text='Show Runway Data', command=ui.button_clicked).pack()
    ttk.Button(root, text='Show UK Airport Frequency Data', command=ui.button_clicked).pack()
    
    # create button to implement destroy()
    ttk.Button(root, text="Quit", command=root.destroy).pack()

    # create event binding, press esc to exit
    root.bind('<Escape>', lambda e: close_win(e, root= root))

    #closing function
    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            root.destroy()
    # an event to close window
    def close_win(e, root:tk.Tk):
        root.destroy()

    # fix blur in ui
    try:
        from ctypes import windll

        windll.shcore.SetProcessDpiAwareness(1)
    finally:
        root.protocol("WM_DELETE_WINDOW", on_closing)
        root.mainloop()



    
    root.mainloop()
