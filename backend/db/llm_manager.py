# llm_api_manager.py
from flask import Flask, jsonify, request
from pymongo import MongoClient
from pymongo.errors import PyMongoError
import threading
from bson import ObjectId

app = Flask(__name__)

class LLMAPIManager:
    def __init__(self, mongo_uri, db_name, collection_name):
        self.mux = threading.RLock()
        self.client = MongoClient(mongo_uri)
        self.collection = self.client[db_name][collection_name]
        self.apis = []
        self.load_from_db()

    def add_api(self, llm_api, wallet_address, other_info):
        for api in self.apis:
            if api['llm_api'] == llm_api:
                print(f"API already exists, update it using new: {api}")  # 调试信息
                api['llm_api'] = llm_api
                return
        with self.mux:
            api_info = {
                "llm_api": llm_api,
                "wallet_address": wallet_address,
                "other_info": other_info
            }
            self.apis.append(api_info)
            self.save_to_db()

    def save_to_db(self):
        with self.mux:
            try:
                self.collection.delete_many({})
                for info in self.apis:
                    self.collection.insert_one(info)
            except PyMongoError as e:
                print(f"Error saving to database: {e}")

    def load_from_db(self):
        with self.mux:
            try:
                for document in self.collection.find():
                    self.apis.append({
                        "llm_api": document['llm_api'],
                        "wallet_address": document['wallet_address'],
                        "other_info": document['other_info'],
                    })
            except PyMongoError as e:
                print(f"Error loading from database: {e}")

    def get_api_info(self):
        print(f"Current APIs: {self.apis}")  # 调试信息
        return self.apis

llm_api_manager = LLMAPIManager("mongodb://localhost:27017", "hobbit", "llm_apis")

@app.route('/apis', methods=['GET'])
def get_apis():
    return jsonify(llm_api_manager.get_api_info()), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)