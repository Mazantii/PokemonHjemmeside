import pymongo
from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://joakimmazanti:irtmHR42oloXdpAJ@cluster0.v75mvtn.mongodb.net/?retryWrites=true&w=majority")
db = cluster["pokemon"]
collection = db["storage"]

#Post the data to MongoDB
post = {"name": "Pikachu", "buy_price": 30, "sold_price": 65, "my_evaluation": "NM",  "amount": 1}
collection.insert_one(post)



