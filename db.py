import pymongo
from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://joakimmazanti:irtmHR42oloXdpAJ@cluster0.v75mvtn.mongodb.net/?retryWrites=true&w=majority")
db = cluster["pokemon"]
collection = db["storage"]

#Post the data to MongoDB
def PostData(name, buy_price, sold_price, my_evaluation, amount, hjemme, pokemon_id, holo, comment):
    post = {"name": name, "buy_price": buy_price, "sold_price": sold_price, "my_evaluation": my_evaluation,  
    "amount": amount, "hjemme": hjemme, "pokemon_id": pokemon_id, "holo": holo, "comment": comment}
    collection.insert_one(post)

#PostData("seiuhiuhe", 100, 200, "Near Mint", 1, Hjemme, "XY12", "Holo", "")
#For all of the data in the collection find the ones with amount 1 or above and make them into a array
available = {}
not_home = {}

#This is for the cards that are at home
def GiveAvailable():
    for x in collection.find():
        if x["amount"] >= 1:
            #if there is a match make a new object in the available array with the name as the key and the sold_price, my_evaluation and amount as the value
            available[x["name"]] = [x["sold_price"], x["my_evaluation"], x["amount"], x["hjemme"], x["buy_price"], x["pokemon_id"],
             x["holo"], x["comment"]]
    return available

#This is for the card that are out being sold
def NotHome():
    #Make a new array containing all of the cards that are "Ude" and have a amount of 1 or more
    for x in collection.find():
        if x["hjemme"] == "Ude" and x["amount"] >= 1:
            not_home[x["name"]] = [x["sold_price"], x["my_evaluation"], x["amount"], x["hjemme"], x["buy_price"], x["pokemon_id"],
             x["holo"], x["comment"]]

#access the name of the first element in the array
print(available)





