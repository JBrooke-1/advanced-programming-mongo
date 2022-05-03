from unicodedata import category
from pymongo import MongoClient, database, collection, cursor, DESCENDING, ASCENDING
from dotenv import load_dotenv
import os
import api.files as files

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


# get all results from a particular database
def find_in_db(
    collection_name: str, search_params: dict = {}, fields_to_return: dict = {}
) -> cursor.Cursor:
    my_collection: collection.Collection = my_db[collection_name]
    result = my_collection.find(search_params, fields_to_return)
    return result


def find_maxmin_val(
    collection_name: str,
    field: str,
    search_params: dict = {},
    fields_to_return: dict = {},
    is_ascending: bool = False,
) -> float:
    my_collection: collection.Collection = my_db[collection_name]

    if not is_ascending:
        result = my_collection.find_one(
            search_params, fields_to_return, sort=[(field, DESCENDING)]
        )
    else:
        result = my_collection.find_one(
            search_params, fields_to_return, sort=[(field, ASCENDING)]
        )

    return result[field]


def find_small_airport_average(collection_name: str, search_params: dict) -> float:
    query = [
        
            {"$match": {"type": "small_airport"}},
            {"$group": {"_id": "$type", "average": {"$avg": "$frequency_mhz"}}},
        
    ]
    my_collection: collection.Collection = my_db[collection_name]
    result = list(my_collection.aggregate(query))
    return result[0]["average"]

def find_big_airport_average_above100(collection_name: str, search_params: dict) -> float:
    query = [
        
            {"$match": {"$and" :[
                        {"type": "large_airport"}, 
                        {"frequency_mhz": {"$gt" : 100}}
                        ]}
            },
            {"$group": {"_id": "$type", "average": {"$avg": "$frequency_mhz"}}},
        
    ]
    my_collection: collection.Collection = my_db[collection_name]
    result = list(my_collection.aggregate(query))
    return result[0]["average"]

