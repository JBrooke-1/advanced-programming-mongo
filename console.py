# code to fix the path import error
import sys, os

dir_path = os.path.dirname(os.path.realpath(__file__))
api_path = ""
for dir in os.listdir(dir_path):
    dir = os.path.join(dir_path, dir)
    if "api" in dir:
        print(dir)
        api_path = dir
        break
sys.path.insert(1, api_path)
print(sys.path)

import api.db as db
import api.files as files
import api.clean_data as clean

if __name__ == "__main__":
    # insert initial data into db
    all_df, df_dict = files.read_csv_files(d_path="data/")

    # clean the data
    # remove all airport data that have a type closed
    df_dict["airports"] = files.remove_closed_type(df_dict, name="airports")

    # create a frequency column
    df_dict["uk-airports-frequencies"] = files.create_freq_col(
        df_dict["airports"], df_dict["airport-frequencies"]
    )

    # delete db collections if already exist
    db.delete_collections(db.my_db)

    # check if the database has been prepopulated
    db.debug_collections(db.my_db)
    print("\n##############\n")

    # insert cleaned data into database
    db.insert_df_to_db(db.my_db, df_dict)
    print("\n##############\n")
    
    # check if the database has been prepopulated
    db.debug_collections(db.my_db)
    print("\n##############\n")

    # convert existing dataframe into json
    print("\n##############\n")
    files.export_to_json(df_dict)
