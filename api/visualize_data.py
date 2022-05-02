import files
import db
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


def draw_small_airport_freq():
    # find all smallairport from the uk airport db
    small_uk_airports = db.find_in_db(
                            collection_name="uk-airports-frequencies",
                            search_params={"type" : "small_airport"},
                            fields_to_return= {"airport_ref": 1, "frequency_mhz" : 1, "name" : 1, "_id" : 0})
    small_uk_airports_max = db.find_maxmin_val(
                            collection_name="uk-airports-frequencies",
                            field = "frequency_mhz",
                            search_params={"type" : "small_airport"},
                            fields_to_return={"frequency_mhz": 1, "_id" : 0})
    
    small_uk_airports_min = db.find_maxmin_val(
                            collection_name="uk-airports-frequencies",
                            is_ascending= True,
                            field = "frequency_mhz",
                            search_params={"type" : "small_airport"},
                            fields_to_return={"frequency_mhz": 1, "_id" : 0})
    print("max herz is", small_uk_airports_max, " and min herz is ", small_uk_airports_min)
    
    average = db.find_average(collection_name="uk-airports-frequencies",
                                field = "small_airport", 
                                category = "frequency_mhz")
    
    print(average)
    # # total width and allocate binsize
    bin_width = 15 # create a set number of bins
    total_width = small_uk_airports_max -small_uk_airports_max
    print('total_width:', total_width)
    bins = int(total_width) // bin_width
    # # create a bin size that reflects the width
    # # get the max frequency value from DB
    # sql_max = """
    #          SELECT MAX(frequency_mhz), airport_ref, db.airports.name FROM db.`airport-frequencies`
    #         JOIN db.airports ON db.airports.id=db.`airport-frequencies`.airport_ref
    #         AND db.airports.type='small_airport';
    #         """
    # max =db.connection.execute(db.text(sql_max))
    # max_val = max.fetchall()[0][0]

    # # get the min frequency value from db
    # sql_min = """
    #         SELECT MIN(frequency_mhz), airport_ref, db.airports.name FROM db.`airport-frequencies`
    #         JOIN db.airports ON db.airports.id=db.`airport-frequencies`.airport_ref
    #         AND db.airports.type='small_airport';
    #         """
    # max =db.connection.execute(db.text(sql_min))
    # min_val = max.fetchall()[0][0]

    # # total width and allocate binsize
    # bin_width = 15 # create a set number of bins
    # total_width = max_val - min_val
    # print('total_width:', total_width)
    # bins = int(total_width) // bin_width

    # # average freqluency
    # sql_avg = """
    #     SELECT AVG(frequency_mhz), airport_ref, db.airports.name FROM db.`airport-frequencies`
    #     JOIN db.airports ON db.airports.id=db.`airport-frequencies`.airport_ref
    #     AND db.airports.type='small_airport';"""
    # avg =db.connection.execute(db.text(sql_avg))
    # avg_val = avg.fetchall()[0][0]

    # # added visualization for historgram
    # counts, edges, bars = plt.hist(x=[result[0] for result in results], bins=400, edgecolor="yellow", color="green")
    plt.xlim(100, avg_val + bin_width)
    plt.bar_label(bars)
    plt.title("communication frequencies used by small_airports")
    plt.xlabel('Frequencies (mhz)')
    plt.ylabel('Numbers of counts')
    plt.show()


draw_small_airport_freq()