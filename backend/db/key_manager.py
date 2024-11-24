import requests
import threading
import json
from pymongo import MongoClient
from pymongo.errors import PyMongoError

class UserBalanceResponse:
    def __init__(self, address, balance):
        self.address = address
        self.balance = balance

class KeyManager:
    def __init__(self, api_url, mongo_uri, db_name, collection_name):
        self.user_keys = {}
        self.mux = threading.RLock()
        self.api_url = api_url
        self.client = MongoClient(mongo_uri)
        self.collection = self.client[db_name][collection_name]
        self.load_from_db()

    def activate_key(self, user_address):
        balance = self.get_user_balance(user_address)
        print(balance)
        if balance <= 0:
            raise ValueError("insufficient tokens to activate key")

        with self.mux:
            self.user_keys[user_address] = True
        self.save_to_db()

    def deactivate_key(self, user_address):
        with self.mux:
            if user_address in self.user_keys:
                del self.user_keys[user_address]
        self.save_to_db()

    def is_key_active(self, user_address):
        with self.mux:
            return self.user_keys.get(user_address, False)

    def get_user_balance(self, user_address):
        response = requests.get(f"{self.api_url}/balance?address={user_address}")
        if response.status_code != 200:
            raise Exception(f"failed to get balance: {response.status_code}")

        balance_response = response.json()
        return balance_response['balance']

    def save_to_db(self):
        with self.mux:
            try:
                self.collection.delete_many({})
                for address, active in self.user_keys.items():
                    self.collection.insert_one({"address": address, "active": active})
            except PyMongoError as e:
                print(f"Error saving to database: {e}")

    def load_from_db(self):
        with self.mux:
            try:
                for document in self.collection.find():
                    self.user_keys[document['address']] = document['active']
            except PyMongoError as e:
                print(f"Error loading from database: {e}")


if __name__ == "__main__":
    api_url = "http://localhost:5000"
    mongo_uri = "mongodb://localhost:27017"
    db_name = "hobbit"
    collection_name = "user_keys"
    km = KeyManager(api_url, mongo_uri, db_name, collection_name)
    km.activate_key("0xaa")
    km.activate_key("0xba")
    km.activate_key("0xca")
    km.save_to_db()
    km.load_from_db()