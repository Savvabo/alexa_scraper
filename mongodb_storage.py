from pymongo import MongoClient, UpdateOne


def connect_to_mongo():
    client = MongoClient('mongodb://localhost', connect=True)['Alexa_scraper']
    return client


class MongoDBStorage:
    def __init__(self):
        self.client = connect_to_mongo()
        self.alexa_collection = self.client['Alexa_scraper']

    def run(self, data: dict, website_name: str):
        data['_id'] = website_name
        self.alexa_collection.update_one({'_id': website_name}, {"$set": data}, upsert=True)

       