from pymongo import MongoClient
from dotenv import load_dotenv
import os
import files

load_dotenv()
MONGO_PORT = int(os.environ.get("MONGO_PORT", 27017))
USER = os.environ.get("MONGODB_ADMINUSERNAME", "admin")
PASSWORD = os.environ.get("MONGODB_ADMINPASSWORD", "pass")
HOST = os.environ.get("MONGO_HOST", "mongo")

# create connection with localhost
client = MongoClient('mongodb://localhost:27017/')

# create a database called demo
db = client["demo"]

# added all collections need by database
airports_collection = db["airports"]
frequency_collection = db["airport-frequencies"]
runways_collection =db["runway"]


# insert initial data into db
all_df, df_dict = files.read_csv_files()

# debug all current collections
for col in db.list_collection_names():
    print(f"currently we have {col} in mongodb")

print("\n##############\n")

# insert into collection when it is not empty
for key, val in df_dict.items():
    collection = db.get_collection(key)
    total_data = len(list(collection.find({})))
    if total_data == 0:
        collection.insert_many(val.to_dict('records'))
    else:
        print(f"currently in {collection.name} we have a total of {total_data} items")

# convert existing dataframe into json
print("\n##############\n")
files.export_to_json(df_dict)

