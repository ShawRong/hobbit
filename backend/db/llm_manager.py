# llm_api_manager.py
from flask import Flask, jsonify, request
import pickle
import os
import threading

app = Flask(__name__)

class LLMAPIManager:
    def __init__(self, data_file='llm_apis.pkl'):
        self.mux = threading.RLock()
        self.data_file = data_file
        self.apis = self.load_from_db()

    def add_api(self, llm_api, wallet_address, other_info):
        for api in self.apis:
            if api['llm_api'] == llm_api:
                print(f"API already exists, delete it first: {api}")  # Debug info
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
                with open(self.data_file, 'wb') as f:
                    pickle.dump(self.apis, f)
            except Exception as e:
                print(f"Error saving to file: {e}")

    def load_from_db(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'rb') as f:
                try:
                    return pickle.load(f)
                except Exception as e:
                    print(f"Error loading from file: {e}")
                    return []
        return []

    def get_api_info(self):
        print(f"Current APIs: {self.apis}")  # Debug info
        return self.apis

    def remove_api(self, llm_api):
        with self.mux:
            for api in self.apis[:]:  # Create a copy of the list to iterate safely
                if api['llm_api'] == llm_api:
                    self.apis.remove(api)
                    self.save_to_db()
                    return True
            return False

llm_api_manager = LLMAPIManager()

@app.route('/apis', methods=['GET'])
def get_apis():
    return jsonify(llm_api_manager.get_api_info()), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
