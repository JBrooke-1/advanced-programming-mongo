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
