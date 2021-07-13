from pymongo import MongoClient

client = MongoClient()

mongo_shop = client['mongo_shop']

items = mongo_shop['items']

# item:
# name
# price
# count
# additional
