import tkinter as tk
from tkinter import CENTER, LEFT, ttk
from tkinter import messagebox
from pymongo import MongoClient, collection

root = tk.Tk()
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


# show all db results
def query_collection_result(col_name="airports"):
    # create connection with localhost
    client = MongoClient("mongodb://localhost:27017/")
    db = client["demo"]
    coll: collection.Collection = db[col_name]
    # turn columns into a dictionary
    columns = list(coll.find_one({}).keys())
    columns.remove("_id")
    print(columns)
    # render tree
    # get current size of main window
    curMainWindowHeight = root.winfo_height()
    curMainWindowWidth = root.winfo_width()

    tree = ttk.Treeview(root, columns=columns, show="headings")
    for key in columns:
        print(key)
        tree.column(key, anchor=CENTER,)
        tree.heading(f"{key}", text=str(key))

    tree.grid(row=1, column=1, sticky=tk.EW)
    # add a scrollbar
    scrollbar_vert = ttk.Scrollbar(root, orient=tk.VERTICAL, command=tree.yview)
    scrollbar_horz = ttk.Scrollbar(root, orient=tk.HORIZONTAL, command=tree.xview)
    tree.configure(yscrollcommand=scrollbar_vert.set, xscrollcommand=scrollbar_horz)
    scrollbar_vert.grid(row=1, column=2, sticky="ns")
    scrollbar_horz.grid(row=2, column=1, sticky="we")

    # In command show_button() function is passed to recover Button B1
    back_button = tk.Button(root, text="Button 3", command=tree.state("disabled"))
    back_button.grid(column=2, row=3, sticky=tk.SW, padx=1, pady=1)

def create_main_window(window_width=1200, window_height = 600):
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

def start_window():
     # fix blur in ui
    try:
        from ctypes import windll

        windll.shcore.SetProcessDpiAwareness(1)
    finally:
        root.protocol("WM_DELETE_WINDOW", on_closing)
        root.mainloop()

if __name__ == "__main__":
    
    create_main_window()

    # createa the container grid
    root.columnconfigure(0, weight=3)
    root.columnconfigure(1, weight=6)
    root.columnconfigure(2, weight=6)
    # place a label on the root window
    message = tk.Label(root, text="Airport Data Analysis", font=("Times New Roman", 18))
    message.grid(column=1, row=0, sticky=tk.EW, padx=5, pady=5)

    # create a button to show airport data
    all_data = ttk.Button(
        root, text="Show All Airport Data", command=query_collection_result
    )
    all_data.grid(column=0, row=1, sticky=tk.EW, padx=1, pady=1)

    # frequency data button
    freq_data = ttk.Button(root, text="show Frequency Data", command=query_collection_result)
    freq_data.grid(column=0, row=2, sticky=tk.EW, padx=1, pady=1)

    # runway data button
    runway_data = ttk.Button(root, text="Show Runway Data", command=query_collection_result)
    runway_data.grid(column=0, row=3, sticky=tk.EW, padx=1, pady=1)

    # uk data
    uk_airport_data = ttk.Button(
        root, text="Show UK Airport Frequency Data", command=query_collection_result
    )
    uk_airport_data.grid(column=0, row=4, sticky=tk.EW, padx=1, pady=1)

    # create button to implement destroy()
    quit_button = ttk.Button(root, text="Quit", command=on_closing)
    quit_button.grid(column=0, row=5, sticky=tk.EW, padx=1, pady=1)

    # create event binding, press esc to exit
    root.bind("<Escape>", lambda e: close_win(e, root=root))

    start_window()
   


