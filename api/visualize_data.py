import files
import db
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


def draw_small_airport_freq():
    # find all smallairport from the uk airport db
    small_uk_airports = db.find_in_db(
        collection_name="uk-airports-frequencies",
        search_params={"type": "small_airport"},
        fields_to_return={"airport_ref": 1, "frequency_mhz": 1, "name": 1, "_id": 0},
    )
    small_uk_airports_max = db.find_maxmin_val(
        collection_name="uk-airports-frequencies",
        field="frequency_mhz",
        search_params={"type": "small_airport"},
        fields_to_return={"frequency_mhz": 1, "_id": 0},
    )

    small_uk_airports_min = db.find_maxmin_val(
        collection_name="uk-airports-frequencies",
        is_ascending=True,
        field="frequency_mhz",
        search_params={"type": "small_airport"},
        fields_to_return={"frequency_mhz": 1, "_id": 0},
    )
    print(
        "max herz is", small_uk_airports_max, " and min herz is ", small_uk_airports_min
    )

    average = db.find_small_airport_average(
        collection_name="uk-airports-frequencies",
        search_params={"type": "small_airport"},
    )
    print(average)

    # draw the final result
    draw_result(
        small_uk_airports,
        min_val=small_uk_airports_min,
        max_val=small_uk_airports_max,
        average=average,
        title="communication frequencies used by uk's small_airports"
    )


def draw_result(query_result, min_val, max_val, average, title):

    # # total width and allocate binsize
    bin_width = 15  # create a set number of bins
    total_width = max_val - min_val
    print("total_width:", total_width)
    bins = int(total_width) // bin_width

    # visualize the historgram
    counts, edges, bars = plt.hist(
        x=[result["frequency_mhz"] for result in list(query_result)],
        bins=400,
        edgecolor="yellow",
        color="green",
    )
    plt.xlim(110, average + bin_width)
    plt.bar_label(bars)

    # draw an average line
    min_ylim, max_ylim = plt.ylim()
    plt.axvline(average, color="k", linestyle="dashed", linewidth=1)
    plt.title(title)
    plt.text(average * 1.1, max_ylim * 0.9, "Mean: {:.2f}".format(average))

    # add label to the table
    plt.xlabel("Frequencies (mhz)")
    plt.ylabel("Numbers of counts")
    plt.show()


draw_small_airport_freq()

