import tkinter as tk
from tkinter import CENTER, LEFT, ttk
from pymongo import MongoClient, collection, database
import api.airport_visualisation as airport_visuals, api.correlation_analysis as freq_col
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

LARGE_FONT = ("Verdana", 12)

# draw plots
def show_small_airport():
    airport_visuals.draw_small_airport_freq()
    airport_visuals.plt.show()


def show_big_airport():
    airport_visuals.draw_big_airport_freq()
    airport_visuals.plt.show()


# class that works with graphs
class CorrelationAnalysis(tk.Frame):
    def __init__(self, parent, controller):

        # greeting page
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Frequency Correlation", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        # return to home page
        button1 = tk.Button(
            self, text="Back to Home", command=lambda: controller.show_frame(StartPage)
        )
        button1.pack()
        label = tk.Label(self, text="All airport data", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        # show graphs
        fig = freq_col.analyze_freq_correlation()
        canvas = FigureCanvasTkAgg(fig, master=self)  # A tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().pack()


# class that works with graphs
class Small_AirPort_Data_Visual(tk.Frame):
    def __init__(self, parent, controller):

        # greeting page
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Small Airport Frequency", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        # return to home page
        button1 = tk.Button(
            self, text="Back to Home", command=lambda: controller.show_frame(StartPage)
        )
        button1.pack()

        # show graphs
        fig = airport_visuals.draw_small_airport_freq()
        canvas = FigureCanvasTkAgg(fig, master=self)  # A tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().pack()


# class that works with graphs
class Big_AirPort_Data_Visual(tk.Frame):
    def __init__(self, parent, controller):

        # greeting page
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Large Airport Frequency", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        # return to home page
        button1 = tk.Button(
            self, text="Back to Home", command=lambda: controller.show_frame(StartPage)
        )
        button1.pack()

        # show graphs
        fig = airport_visuals.draw_big_airport_freq()
        canvas = FigureCanvasTkAgg(fig, master=self)  # A tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().pack()


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
        docs = coll.find({})[:200]  # return top 200 results
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
        scroll_bar_v = tk.Scrollbar(self, orient="vertical")
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
            tree.insert("", tk.END, values=r)

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
            self, text="Runway Data", command=lambda: controller.show_frame(RunwayPage)
        )
        button2.pack()

        freq_button = tk.Button(
            self,
            text="All Frequency Data",
            command=lambda: controller.show_frame(FreqPage),
        )
        freq_button.pack()

        uk_airport_freq_button = tk.Button(
            self,
            text="UK Small Medium Large Airport Frequency Data",
            command=lambda: controller.show_frame(UKFreqPage),
        )
        uk_airport_freq_button.pack()

        small_freq_button = tk.Button(
            self,
            text="Small Airport Frequencies",
            command=lambda: controller.show_frame(Small_AirPort_Data_Visual),
        )
        small_freq_button.pack()

        big_freq_button = tk.Button(
            self,
            text="Show Large UK Airport Frequencies",
            command=lambda:controller.show_frame(Big_AirPort_Data_Visual),
        )
        big_freq_button.pack()

        corr_freq_button = tk.Button(
            self,
            text="Correlation Between Airports and Frequencies",
            command=lambda: controller.show_frame(CorrelationAnalysis),
        )
        corr_freq_button.pack()


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


class RunwayPage(PageWithDB):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # return to home page
        button1 = tk.Button(
            self, text="Back to Home", command=lambda: controller.show_frame(StartPage)
        )
        button1.pack()
        label = tk.Label(self, text="All Runway Data", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        self.collection_name = "runways"
        # visualize airport data
        self.draw_table()


class FreqPage(PageWithDB):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # return to home page
        button1 = tk.Button(
            self, text="Back to Home", command=lambda: controller.show_frame(StartPage)
        )
        button1.pack()
        label = tk.Label(self, text="Frequency for all airports", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        self.collection_name = "airport-frequencies"
        # visualize airport data
        self.draw_table()


class UKFreqPage(PageWithDB):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # return to home page
        button1 = tk.Button(
            self, text="Back to Home", command=lambda: controller.show_frame(StartPage)
        )
        button1.pack()
        label = tk.Label(
            self, text="UK Small Medium Large Airport Frequency Data", font=LARGE_FONT
        )
        label.pack(pady=10, padx=10)
        self.collection_name = "uk-airports-frequencies"
        # visualize airport data
        self.draw_table()


class MainUI(tk.Tk):
    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (
            StartPage,
            AirportPage,
            RunwayPage,
            FreqPage,
            UKFreqPage,
            CorrelationAnalysis,
            Small_AirPort_Data_Visual,
            Big_AirPort_Data_Visual,
        ):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()
