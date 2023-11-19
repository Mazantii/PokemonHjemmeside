from flask import Flask, render_template
import main
import db


#Run the UpdateSales function
main.UpdateSales()

#values from main.py
earnings = main.earnings
amount = main.total_amount_of_sales

#values from db.py
available = db.available
not_available = db.not_home

#Run the GiveAvailable function
db.GiveAvailable()


app = Flask(__name__)

@app.route("/")
def home():
    #Send the earnings to the index.html file
    return render_template("index.html", earnings=earnings, sales=amount, not_available=not_available)

@app.route("/database")
def database():
    #Send the earnings to the index.html file
    return render_template("database.html", available=available)

if __name__ == "__main__":
    app.run(debug=True)