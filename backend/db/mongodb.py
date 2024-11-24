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

def create_collection(db_name, collection_name):
    client = connect_to_mongo()  # 连接到 MongoDB
    db = client[db_name]  # 选择数据库
    try:
        collection = db.create_collection(collection_name)  # 创建集合
        logging.info(f"Collection '{collection_name}' created in database '{db_name}'.")
        return collection
    except Exception as err:
        logging.error(f"Error creating collection: {err}")
        raise


