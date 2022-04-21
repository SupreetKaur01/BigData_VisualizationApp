import pymongo
from pymongo.errors import ConnectionFailure
from pymongo import MongoClient
import json

def getLocalHandler():
    """ Connect to MongoDB """
    try:
        client=MongoClient()
        #c = Connection(host="localhost", port=27017)
        db=client.tweet_db
        tweet_collection=db.tweet_collection
        tweet_collection.create_index([("id",pymongo.ASCENDING)],unique=True)

        # Loading or Opening the json file
        with open('C:/Users/supre/Downloads/algorand_json.json', encoding='utf8') as file:
            file_data = json.load(file)

        # Inserting the loaded data in the Collection
        # if JSON contains data more than one entry
        # insert_many is used else inser_one is used
        if isinstance(file_data, list):
            tweet_collection.insert_many(file_data)  
        else:
            tweet_collection.insert_one(file_data)

    except ConnectionFailure as e:
        print ("Could not connect to MongoDB: %s" % e)
        return False
    
    # Get a Database handle to a database named "---param---"
    dbh = client[tweet_collection]
    # Demonstrate the db.connection property to retrieve a reference to the
    # Connection object should it go out of scope. In most cases, keeping a
    # reference to the Database object for the lifetime of your program should
    # be sufficient.
    assert dbh.connection == client
    print("Successfully set up a local database handle")
    return dbh