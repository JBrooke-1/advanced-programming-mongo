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

    def get_all_records(self):
        coll: collection.Collection = self.db[self.collection_name]
        docs = coll.find({})[:200] # return top 200 results
        rows = []
        for item in docs:
            val = list(item.values())
            val = val[1:]
            print(val)
            rows.append(val)
        print(rows)
        return rows[1:]
    
    def draw_table(self):
        # render all columns
        columns = self.get_col_names()

        # scrollbar
        scroll_bar_v = tk.Scrollbar(self,  orient="vertical")
        scroll_bar_v.pack(side=tk.RIGHT, fill=tk.Y)

        scroll_bar_h = tk.Scrollbar(self, orient="horizontal")
        scroll_bar_h.pack(side=tk.BOTTOM, fill=tk.X)

        tree = ttk.Treeview(
            self,
            columns=columns,
            show="headings",
            xscrollcommand=scroll_bar_h.set,
            yscrollcommand=scroll_bar_v.set,
        )

        # render table columns
        for key in columns:
            print(key)
            tree.column(
                key, anchor=CENTER,
            )
            tree.heading(f"{key}", text=str(key))

        # render table values
        records = self.get_all_records()
        for r in records:
            tree.insert('', tk.END, values=r)

        # pack the data and configuer the view
        tree.pack()
        scroll_bar_v.config(command=tree.yview)
        scroll_bar_h.config(command=tree.xview)


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
        # visualize airport data
        self.draw_table()
        


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
