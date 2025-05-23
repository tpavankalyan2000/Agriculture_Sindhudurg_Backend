from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

class MongoDB:
    def __init__(self, uri=None, db_name=None):
        self.uri = uri or os.getenv("MONGO_URI")
        self.db_name = db_name or os.getenv("MONGO_DB_NAME")
        self.client = MongoClient(self.uri)
        self.db = self.client[self.db_name]

        self.users = self.db["users"]
        self.forest_incidents = self.db["forest_incidents"]
        self.forest_prediction = self.db['forest_prediction']

    def close(self):
        if self.client:
            self.client.close()