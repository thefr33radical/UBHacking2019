import pymongo
import dns
import json
import models

steps = 10

class Database(object):
    def __init__(self):
        with open("./global.config") as f:
            self.config = json.load(f)
        self.client = pymongo.MongoClient(self.config["db_url"])
        self.db = self.client.model_db
        self.models = self.db.models

    def add_to_db(self, obj):
        self.models.insert_one(obj)

if __name__ == "__main__":
    # Initialize the database
    db = Database()

    # Grab models
    models = models.Models("\data\data_ub.csv")

    # Run the models
    uni_baseline = models.uni_baseline(steps)
    #uni_sarima = models.uni_sarima(steps)
    print(uni_baseline)
    # Add results to database
    db.add_to_db(uni_baseline)
    #db.add_to_db(uni_sarima)
