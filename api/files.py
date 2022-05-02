import os
import pandas as pd
from pathlib import Path


# helper function used to read and iterate through
def read_csv_files(d_path="../data"):
    dfs_only = []
    dfs_dict = {}
    if os.path.isdir(d_path):
        dirs = [os.path.join(d_path, f) for f in os.listdir(d_path)]
        print(dirs)
        for file in dirs:
            if file.endswith(".csv"):
                val = pd.read_csv(file)
                dfs_only.append(val)
                key = Path(file).stem
                dfs_dict[key] = val
        return pd.concat(dfs_only), dfs_dict


# function to convert csv to json
def export_to_json(df_dict, dir="../json_data/"):
    if not os.path.isdir(dir):
        os.mkdir(dir)

    # make every key into dataframe
    for key in df_dict:
        val = df_dict[key]
        file = f"{dir}{key}.json"

        # if the value is an instance of dataframe
        # then convert it into json file
        if isinstance(val, pd.DataFrame):
            val.to_json(file)
            print(f"{file} has been created successfully")


# test if the 'closed' type is still in the databse
def remove_closed_type(df, name, val="closed", col="type"):
    df = df[name]
    if isinstance(df, pd.DataFrame):
        if col in df.columns:
            # using drop function to drop  rows basing on column value
            results = df[df[col] == val]
            print(results)
            df.drop(results.index, inplace=True)
            count = len(results.index)  # total count of indexes
            # print a test statement
            print(
                f"""{val} has been removed from 
                the column {col}, 
                a total of {count} values"""
            )
            return df
        else:
            print(f"f{col} is not in {name}")


# create a new df by frequency and add it to json
# since python 3.6 you can define static typing
def create_freq_col(airports_df: pd.DataFrame, freq_df: pd.DataFrame, dir:str="../data") -> pd.DataFrame:
    # using all to loop through list
    if not (airports_df.empty or freq_df.empty):
        types = ["large_airport", "medium_airport", "small_airport"]
        countries = ["GB"]
        useful_cols = [
            "type",
            "name",
            "id",
            "iso_country",
            "latitude_deg",
            "longitude_deg",
        ]
        sml_airports: pd.DataFrame = airports_df.filter(items=useful_cols)

        # all airport data rows matching the search result
        sml_airports = sml_airports[
            (sml_airports["type"].isin(types))
            & (sml_airports["iso_country"].isin(countries))
        ]
        print("\n return top 3 resutls: ", sml_airports.head(3), "\n")

        # combine airport and frequency dataframe toproduce new dataframe
        uk_sml_freqs: pd.DataFrame = pd.merge(
            sml_airports, freq_df, left_on="id", right_on="airport_ref"
        )
        print("all cols of new df: ", uk_sml_freqs.columns)

        # drop and rename some colulm names
        uk_sml_freqs = uk_sml_freqs.drop(["id_x", "id_y"], axis=1)
        uk_sml_freqs = uk_sml_freqs.rename(
            columns={"type_x": "type", "type_y": "freq_type"},
        )
        print("testing uk sml airport frequency \n", uk_sml_freqs.head(5))

        # convert such dataframe to csv in data folder
        uk_sml_freqs.to_csv(dir, index=False)
        return uk_sml_freqs
    else:
        pass  # does nothing

