import api.db as db
import api.files as files
import api.clean_data as clean

if __name__ =='__main__':
    # insert initial data into db
    all_df, df_dict = files.read_csv_files()

    # clean the data
    # remove all airport data that have a type closed
    df_dict["airports"] = files.remove_closed_type(df_dict, name="airports")

    # check if the database has been prepopulated
    db.debug_collections(db.my_db)
    print("\n##############\n")

    # insert cleaned data into database
    db.insert_df_to_db(db.my_db, df_dict)
    print("\n##############\n")

    # convert existing dataframe into json
    print("\n##############\n")
    files.export_to_json(df_dict)
