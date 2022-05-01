from dataclasses import dataclass
import tkinter as tk
from tkinter import CENTER, LEFT, ttk
from pymongo import MongoClient, collection, database

LARGE_FONT = ("Verdana", 12)


class PageWithDB(tk.Frame):
    client = MongoClient("mongodb://localhost:27017/")
    db = client["demo"]
    collection_name: collection.Collection

    def __init__(self, parent):
        super().__init__(self, parent)

    def get_col_names(self):
        coll: collection.Collection = self.db[self.collection_name]
        # turn columns into a dictionary
        columns = list(coll.find_one({}).keys())
        columns.remove("_id")
        return columns


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Welcome to Airport Data", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button = tk.Button(
            self,
            text="All Airport Data",
            command=lambda: controller.show_frame(AirportPage),
        )
        button.pack()

        button2 = tk.Button(
            self, text="UK Airport Data", command=lambda: controller.show_frame(PageTwo)
        )
        button2.pack()


class AirportPage(PageWithDB):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # return to home page
        button1 = tk.Button(
            self, text="Back to Home", command=lambda: controller.show_frame(StartPage)
        )
        button1.pack()
        label = tk.Label(self, text="All airport data", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        self.collection_name = "airports"

        # render all columns
        columns = self.get_col_names()

        # add horizontal and vertical scrollbar
        # scrollbar
        scroll_bar = tk.Scrollbar(self)
        scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)

        scroll_bar = tk.Scrollbar(self, orient="horizontal")
        scroll_bar.pack(side=tk.BOTTOM, fill=tk.X)

        tree = ttk.Treeview(
            self,
            columns=columns,
            show="headings",
            xscrollcommand=scroll_bar.set,
            yscrollcommand=scroll_bar.set,
        )
        for key in columns:
            print(key)
            tree.column(
                key, anchor=CENTER,
            )
            tree.heading(f"{key}", text=str(key))
        
        # pack the data and configuer the view
        tree.pack()
        scroll_bar.config(command=tree.yview)
        scroll_bar.config(command=tree.xview)


class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page Two!!!", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = tk.Button(
            self, text="Back to Home", command=lambda: controller.show_frame(StartPage)
        )
        button1.pack()

        button2 = tk.Button(
            self, text="Page One", command=lambda: controller.show_frame(AirportPage)
        )
        button2.pack()


class MainUI(tk.Tk):
    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, AirportPage, PageTwo):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()
