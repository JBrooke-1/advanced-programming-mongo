import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import api.files as files
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def analyze_freq_correlation(file_path="data/uk-airports-frequencies.csv") -> Figure:
    # clean df
    abs_file_path = files.get_parent_folder(file_path)
    freq_df: pd.DataFrame = pd.read_csv(abs_file_path)

    # only keep relevant columns
    freq_df_original = freq_df[["type", "frequency_mhz"]]
    cleaned_freq_df = freq_df[["type", "frequency_mhz"]]
    cleaned_freq_df["type"], uniques = pd.factorize(cleaned_freq_df["type"])
    freq_df_original["codes"] = cleaned_freq_df["type"]
    print("all unique categories are: ", uniques)
    print("after clean the new dataset is: ", cleaned_freq_df.head())

    # analyze the correlation between airport size and frequency
    correlations_pearson = cleaned_freq_df.corr(method="pearson")
    print("pearson correlation matrix \n", correlations_pearson, "\n")

    # visualize correlation in matplotlib
    return generate_plot(freq_df_original)


def generate_plot(freq_df_original: pd.DataFrame):
    figure = plt.Figure(figsize=(6, 5), dpi=100)
    colors = {
        "small_airport": "red",
        "medium_airport": "blue",
        "large_airport": "green",
    }
    ax = figure.add_subplot(111)  # create 1 by 1 grid
    plot = ax.scatter(
        freq_df_original["type"],
        freq_df_original["frequency_mhz"],
        c=freq_df_original["type"].map(colors),
        label=freq_df_original["type"],
    )
    return figure
