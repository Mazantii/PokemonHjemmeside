import pymongo
from pymongo import MongoClient
import requests

cluster = MongoClient("mongodb+srv://joakimmazanti:irtmHR42oloXdpAJ@cluster0.v75mvtn.mongodb.net/?retryWrites=true&w=majority")
db = cluster["pokemon"]
collection = db["storage"]
sold_storage = db["Sold_Storage"]

def get_pokemon_card_info(card_id):
    api_url = f'https://api.pokemontcg.io/v2/cards/{card_id}'
    headers = {'X-Api-Key': '999933d6-fe39-47ae-9202-7541499b68ff'}

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        card_data = response.json()
        image_url = card_data.get('data', {}).get('images', {}).get('small')

        return {
            'name': card_data.get('data', {}).get('name'),
            'image_url': image_url
        }

    print(f"Error: Unable to fetch information for card ID '{card_id}'")
    return {'image_url': "Image not found"}

# Example: Get information for a specific Pokémon card using its ID
#card_id = 'xy1-1'
#pokemon_info = get_pokemon_card_info(card_id)

#Post the data to MongoDB
def PostData(name, buy_price, sold_price, my_evaluation, amount, hjemme, pokemon_id, holo, comment, image):
    #Find the image using the pokemon tcg api and the pokemon_id
    image = get_pokemon_card_info(pokemon_id)["image_url"]
    post = {"name": name, "buy_price": buy_price, "sold_price": sold_price, "my_evaluation": my_evaluation,  
    "amount": amount, "hjemme": hjemme, "pokemon_id": pokemon_id, "holo": holo, "comment": comment, "image": image}
    collection.insert_one(post)

#PostData("seiuhiuhe", 100, 200, "Near Mint", 1, Hjemme, "XY12", "Holo", "")
#For all of the data in the collection find the ones with amount 1 or above and make them into a array
available = {}
not_home = {}
sold = {}
key_statistics = {}

#This is for the cards that are at home
def GiveAvailable():
    available.clear()
    for x in collection.find():
        if x["amount"] > 0:
            #if there is a match make a new object in the available array with the name as the key and the sold_price, my_evaluation and amount as the value
            available[x["_id"]] = [x["name"] ,x["sold_price"], x["my_evaluation"], x["amount"], x["hjemme"], x["buy_price"], x["pokemon_id"],
             x["holo"], x["comment"], x["image"]]
    print(available)
    return available

#This is for the card that are out being sold
def NotHome():
    not_home.clear()
    #Make a new array containing all of the cards that are "Ude" and have a amount of 1 or more
    for x in collection.find():
        if x["hjemme"] == "Ude" and x["amount"] > 0:
            not_home[x["_id"]] = [x["name"], x["sold_price"], x["my_evaluation"], x["amount"], x["hjemme"], x["buy_price"], x["pokemon_id"],
             x["holo"], x["comment"], x["image"]]

#This is for getting all sold cards
def GetSold():
    sold.clear()

    entities = sold_storage.find().sort("_id", pymongo.DESCENDING)

    for x in entities:
        sold[x["_id"]] = [x["name"], x["sold_price"], x["amount"], x["buy_price"], x["image"], x["time"], x["profit"]]
    return sold

#This is for deleting a card from the database
def DeleteCard(name, pokemon_id):
    #Find the card with the name and pokemon_id and delete it
    collection.delete_one({"name": name, "pokemon_id": pokemon_id})

    #Cleanup
    DeleteZero()

#This is for updating a card as sold
def SoldCard(name, buy_price, sold_price, profit, image, time, amount, pokemon_id):
    #Find the card with the name and pokemon_id and minus the amount by 1, But if the amount is 1 or less already then delete the card
    card = collection.find_one({"name": name, "pokemon_id": pokemon_id})
    if card["amount"] > 0:
        collection.update_one({"name": name, "pokemon_id": pokemon_id}, {"$inc": {"amount": -1}})
    elif card["amount"] == 1:
        collection.delete_one({"name": name, "pokemon_id": pokemon_id})

    # collection.update_one({"name": name, "pokemon_id": pokemon_id}, {"$inc": {"amount": -1}})
    #Create a entry in the sold_storage collection
    sold_storage.insert_one({
        "name": name, 
        "buy_price": buy_price, 
        "sold_price": sold_price,
        "profit": profit,
        "image": image,
        "time": time,
        "amount": 1
    })

    #Cleanup
    DeleteZero()

#This is for generating numbers for the key statistics
#Key Statistics:
#Total sales
#Total money spent in total
#Total profit
#Total cards currently for sale and their current value
def KeyStatistics():
    key_statistics.clear()
    #Total sales
    total_sales = sold_storage.count_documents({})
    key_statistics["total_sales"] = total_sales

    #Total money spent in total
    total_spent = 0
    for x in collection.find():
        total_spent += x["buy_price"] * x["amount"]
    key_statistics["total_spent"] = total_spent

    #Total profit
    total_profit = 0
    for x in sold_storage.find():
        total_profit += x["profit"]
    key_statistics["total_profit"] = total_profit

    #Total cards currently for sale and their current value
    total_cards = 0
    total_value = 0
    for x in collection.find():
        total_cards += x["amount"]
        total_value += x["sold_price"] * x["amount"]
    key_statistics["total_cards"] = total_cards
    key_statistics["total_value"] = total_value

    return key_statistics



#This is for deleting card in the collection with the amount == 0
def DeleteZero():
    #Find all of the cards with amount == 0 and delete them
    collection.delete_many({"amount": 0})
    GiveAvailable()
    NotHome()







