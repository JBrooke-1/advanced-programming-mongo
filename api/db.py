from pymongo import MongoClient, database
from dotenv import load_dotenv
import os
import files

load_dotenv()
MONGO_PORT = int(os.environ.get("MONGO_PORT", 27017))
USER = os.environ.get("MONGODB_ADMINUSERNAME", "admin")
PASSWORD = os.environ.get("MONGODB_ADMINPASSWORD", "pass")
HOST = os.environ.get("MONGO_HOST", "mongo")

# create connection with localhost
client = MongoClient("mongodb://localhost:27017/")

# create a database called demo
my_db = client["demo"]

# added all collections need by database
airports_collection = my_db["airports"]
frequency_collection = my_db["airport-frequencies"]
runways_collection = my_db["runway"]


# debug all current collections
def debug_collections(db):
    if isinstance(db, database.Database):
        for col in db.list_collection_names():
            print(f"currently we have {col} in mongodb")
    else:
        print(f"{db} is not a database")


# delete collections
def delete_collections(db: database.Database):
    for col in db.list_collection_names():
        mycol = db[col]
        mycol.drop()
        print(f"{col} has been dropped...")


# insert into collection when it is not empty
def insert_df_to_db(db, df_dict: dict):
    if isinstance(db, database.Database):
        for key, val in df_dict.items():
            if isinstance(val, files.pd.DataFrame):
                collection = db.get_collection(key)
                total_data = len(list(collection.find({})))
                print("total_data", total_data)
                if total_data == 0:
                    collection.insert_many(val.to_dict("records"))
                else:
                    print(
                        f"""currently in {collection.name}
                         we have a total 
                         of {total_data} items"""
                    )
