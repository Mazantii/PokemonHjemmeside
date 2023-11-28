from flask import Flask, render_template, request
import main
import db
from datetime import datetime


#Run the UpdateSales function
main.UpdateSales()

#values from main.py
earnings = main.earnings
amount = main.total_amount_of_sales


#values from db.py
available = db.available
not_available = db.not_home
sold = db.sold

#Get the key statistics info from db.py
key_statistics = db.KeyStatistics()
total_sales = key_statistics["total_sales"]
total_spent = key_statistics["total_spent"]
total_profit = key_statistics["total_profit"]
total_cards = key_statistics["total_cards"]
total_value = key_statistics["total_value"]



app = Flask(__name__)

@app.route("/")
def home():
    db.NotHome()
    db.GetSold()
    #Send the earnings to the index.html file
    return render_template("index.html", earnings=earnings, sales=amount, not_available=not_available, sold=sold)

@app.route("/database")
def database():
    db.GiveAvailable()
    #Send the available array to the database.html file
    return render_template("database.html", available=available)

@app.route("/statistics")
def statistics():
    db.KeyStatistics()
    #Send the length of all sold cards
    sold_amount = len(sold)
    return render_template("statistics.html", total_sales=total_sales, total_spent=total_spent, total_profit=total_profit, total_cards=total_cards, total_value=total_value, sold_amount=sold_amount )

@app.route("/addcard", methods=["POST"])
def addcard():
    #Get the data from the form
    name = request.form["name"]
    buy_price = int(request.form["buy_price"])
    sold_price = int(request.form["sell_price"])
    evaluation = request.form["evaluation"]
    amount = int(request.form["amount"])
    hjemme = request.form["out_home"]
    pokemon_id = request.form["version"]
    holo = request.form["rev_hol"]
    comment = request.form["comment"]
    image = pokemon_id

    print(name, buy_price, sold_price, evaluation, amount, hjemme, pokemon_id, holo, comment, image)
    #Post it to the db!
    db.PostData(name, buy_price, sold_price, evaluation, amount, hjemme, pokemon_id, holo, comment, image)
    #Update the available array
    db.GiveAvailable()
    return render_template("database.html" , available=available)


#Delete card
@app.route("/deletecard", methods=["POST"])
def deletecard():
    #Get the name of the card that is going to be deleted
    name = request.form["card_name"]
    pokemon_id = request.form["pokemon_id"]
    #Delete the card
    db.DeleteCard(name, pokemon_id)
    return render_template("database.html" , available=available)

#Sold card
@app.route("/soldcard", methods=["POST"])
def soldcard():
    name = request.form["card_name"]
    pokemon_id = request.form["pokemon_id"]
    buy_price = int(request.form["buy_price"])
    sold_price = int(request.form["sell_price"])
    image =  request.form["image"]
    amount = int(request.form["amount"])
    profit = int(sold_price - buy_price)
    #Get the date and time
    time = datetime.now()
    #Send it to the db
    db.SoldCard(name, buy_price, sold_price, profit, image, time, amount, pokemon_id)

    return render_template("database.html" , available=available)


if __name__ == "__main__":
    app.run(debug=True)