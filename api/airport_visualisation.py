import api.db as db
import matplotlib.pyplot as plt
import numpy as np


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
    return draw_result_and_return(
        small_uk_airports,
        min_val=small_uk_airports_min,
        max_val=small_uk_airports_max,
        average=average,
        title="communication frequencies used by uk's small_airports",
    )


# draw big airport freq
def draw_big_airport_freq():
    collection_name = "uk-airports-frequencies"
    search_params = {"type": "large_airport", "frequency_mhz": {"$gt": 100}}

    # find all big from the uk airport db
    big_uk_airports = db.find_in_db(
        collection_name=collection_name,
        search_params=search_params,
        fields_to_return={"airport_ref": 1, "frequency_mhz": 1, "name": 1, "_id": 0},
    )

    big_uk_airports_max = db.find_maxmin_val(
        collection_name=collection_name,
        field="frequency_mhz",
        search_params=search_params,
        fields_to_return={"frequency_mhz": 1, "_id": 0},
    )

    big_uk_airports_min = db.find_maxmin_val(
        collection_name=collection_name,
        is_ascending=True,
        field="frequency_mhz",
        search_params=search_params,
        fields_to_return={"frequency_mhz": 1, "_id": 0},
    )

    # print debug message for big airport
    print(
        "For data above 100,max herz is",
        big_uk_airports_max,
        " and min herz is ",
        big_uk_airports_min,
    )

    average = db.find_big_airport_average_above100(
        collection_name=collection_name, search_params=search_params,
    )
    print(average)

    # draw the final result
    return draw_result_and_return(
        big_uk_airports,
        min_val=big_uk_airports_min,
        max_val=big_uk_airports_max,
        average=average,
        title="communication frequencies used by uk's big airports (more than 100)",
    )


def draw_result(query_result, min_val, max_val, average, title, bin_mod=10):

    # # total width and allocate binsize
    bin_width = 15  # create a set number of bins
    total_width = max_val - min_val
    print("total_width:", total_width)
    bins = int(total_width) // bin_width

    # calculated best number of bins needed
    data_list = [
        result["frequency_mhz"]
        for result in list(query_result)
        if result["frequency_mhz"] is not None
    ]

    # sort the data from min to max
    data_list.sort()
    data_arr = np.array(data_list)
    data_list = reject_outliers(data_arr, m=2).tolist()
    my_bins = np.histogram_bin_edges(data_list, bins="auto", range=(min_val, max_val))

    # visualize the historgram
    counts, edges, bars = plt.hist(
        x=data_list, bins=my_bins, edgecolor="yellow", color="green",
    )
    plt.xlim(data_list[0] - bin_mod, data_list[-1] + bin_mod)
    plt.bar_label(bars)

    # draw an average line
    min_ylim, max_ylim = plt.ylim()
    plt.axvline(average, color="r", linestyle="dashed", linewidth=1)
    plt.title(title)
    plt.text(average, max_ylim * 0.8, "Mean: {:.2f}".format(average), color="r")

    # calculate and draw median
    median = np.median(np.array(data_list))
    plt.axvline(median, color="b", linestyle="dashed", linewidth=1)
    plt.text(median, max_ylim * 0.5, "Median: {:.2f}".format(median), color="b")

    # calculate and draw mode
    mode = max(set(data_list), key=data_list.count)
    plt.plot(mode, max_ylim * 0.2, marker="o", markersize=10, markeredgecolor="red")
    plt.text(mode, max_ylim * 0.2, "Mode: {:.2f}".format(mode), color="k")

    # add label to the table
    plt.xlabel("Frequencies (mhz)")
    plt.ylabel("Numbers of counts")


# a function to reject outliners
def reject_outliers(data, m=2.0):
    d = np.abs(data - np.median(data))
    mdev = np.median(d)
    s = d / mdev if mdev else 0.0
    return data[s < m]


def draw_result_and_return(query_result, min_val, max_val, average, title, bin_mod=10):

    # calculated best number of bins needed
    data_list = [
        result["frequency_mhz"]
        for result in list(query_result)
        if result["frequency_mhz"] is not None
    ]

    # sort the data from min to max
    data_list.sort()
    data_arr = np.array(data_list)
    data_list = reject_outliers(data_arr, m=2).tolist()
    my_bins = np.histogram_bin_edges(data_list, bins="auto", range=(min_val, max_val))

    # visualize the historgram

    fig = plt.Figure(figsize=(10,8))
    ax = fig.add_subplot(111)  # create 1 by 1 grid

    counts, edges, bars = ax.hist(
        x=data_list, bins=my_bins, edgecolor="yellow", color="green",
    )
    ax.set_xlim(data_list[0] - bin_mod, data_list[-1] + bin_mod)
    ax.bar_label(bars)

    # draw an average line
    min_ylim, max_ylim = ax.set_ylim()
    ax.axvline(average, color="r", linestyle="dashed", linewidth=1)
    ax.set_title(title)
    ax.text(average, max_ylim * 0.8, "Mean: {:.2f}".format(average), color="r")

    # calculate and draw median
    median = np.median(np.array(data_list))
    ax.axvline(median, color="b", linestyle="dashed", linewidth=1)
    ax.text(median, max_ylim * 0.5, "Median: {:.2f}".format(median), color="b")

    # calculate and draw mode
    mode = max(set(data_list), key=data_list.count)
    ax.plot(mode, max_ylim * 0.2, marker="o", markersize=10, markeredgecolor="red")
    ax.text(mode, max_ylim * 0.2, "Mode: {:.2f}".format(mode), color="k")

    # add label to the table
    ax.set_xlabel("Frequencies (mhz)")
    ax.set_ylabel("Numbers of counts")

    # return result
    return fig
