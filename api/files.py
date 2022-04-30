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
