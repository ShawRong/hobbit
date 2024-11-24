# Converted Python code for MongoDB connection

from pymongo import MongoClient
import logging

def connect_to_mongo():
    client_options = "mongodb://localhost:27017"
    try:
        client = MongoClient(client_options)
        return client
    except Exception as err:
        logging.error(err)
        raise


