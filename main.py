import datetime
from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


#Login information to Loppemodul.dk
email = 'JoakimMazanti@gmail.com'
password = 'nokianokia1'

#Login information to MongoDB
cluster = MongoClient("mongodb+srv://joakimmazanti:irtmHR42oloXdpAJ@cluster0.v75mvtn.mongodb.net/?retryWrites=true&w=majority")
db = cluster["pokemon"]
collection = db["Last_Sold"]
storage = db["storage"]
sold_storage = db["Sold_Storage"]


#make a function for all of the updating of the sale
def UpdateSales():
    #Create a session
    driver = webdriver.Chrome()

    #Find the Email and Password fields and send the login information
    driver.get("https://loppemodul.dk/auth/login")
    driver.find_element("id", "email").send_keys(email)
    driver.find_element("id", "password").send_keys(password)

    #Find the login button
    button = driver.find_element("css selector","button.btn.btn-primary")

    #Click the login button
    button.click()

    #Set prevous individual sales to the collection in MongoDB 

    #######################################Find total Earnings this week#############################################
        #Find div with class "statcard statcard-success mb-md-0 mb-4 p-4"
    statcard_total_earnings = driver.find_element("css selector", "div.statcard.statcard-success.mb-md-0.mb-4.p-4")
    #Find the h3 element inside of the div
    global earnings
    earnings = statcard_total_earnings.find_element("css selector", "h3")

    #Remove the "DKK" from the string
    earnings = earnings.text.replace("DKK", "")
    #Replace the "," with "."
    earnings = earnings.replace(",", ".")
    # turn the string into an float
    earnings = float(earnings) ##Here we have how much we have sold this week as a float and after commission

    #Earnings without commission cut
    no_commission_earnings = earnings / 0.85

    #Find the amount of sales this week
    statcard_total_sales = driver.find_element("css selector", "div.statcard.statcard-success.mb-md-0.mb-2.p-4")
    
    global total_amount_of_sales

    total_amount_of_sales = statcard_total_sales.find_element("css selector", "h3")

    #Turn sales into an int
    total_amount_of_sales = int(total_amount_of_sales.text)


    #######################################Find all individual sales this week#############################################
    #Find the div with all the sales with class "card-body p-0 p-md-4"
    sales_div = driver.find_element("css selector", "div.card-body.p-0.p-md-4")

    #Make an array containing all the tr elements but only with their first td element and the second "small" element in the third td element,
    sales_times = sales_div.find_elements("css selector", "tr td:nth-child(1)")

    #Make an array containing this xpath //*[@id="repeat-object"]/tbody/tr[1]/td[3]/text()
    sales_prices = sales_div.find_elements("xpath", "//*[@id='repeat-object']/tbody/tr/td[3]/small[2]")


    #Remove "85,0% af" and "DKK" from the strings and make it a float
    for i in range(len(sales_prices)):
        sales_prices[i] = sales_prices[i].text.replace("85,0% af", "")
        sales_prices[i] = sales_prices[i].replace("DKK", "")
        sales_prices[i] = sales_prices[i].replace(",", ".")
        sales_prices[i] = float(sales_prices[i])

    #make an array containing this xpath //*[@id="repeat-object"]/tbody/tr[1]/td[3]/small[1]
    global sales_amounts
    sales_amounts = sales_div.find_elements("xpath", "//*[@id='repeat-object']/tbody/tr/td[3]/small[1]")


    #Remove "Antal: " from the strings and make it an int
    for i in range(len(sales_amounts)):
        sales_amounts[i] = sales_amounts[i].text.replace("Antal: ", "")
        sales_amounts[i] = int(sales_amounts[i])

    #Make a object with the sales times, prices and amounts each as their own value inside of it.
    individual_sales = []
    for i in range(len(sales_times)):
        individual_sales.append({"time": sales_times[i].text, "price": sales_prices[i], "amount": sales_amounts[i]})

    #######################################Update the collection of "Last_Sold"#############################################
    ##post the individual sales to mongo db and give it a name called "sales" and a id of 1##
    #collection.insert_one({"_id": 1, "sales": individual_sales})

    #Get only the price value from all the objects in sales array from the database with the id 1
    sales = collection.find_one({"_id": 1})["sales"]
    sales_prices_stored = [i["price"] for i in sales]
    #Turn the sale prices into ints
    sales_prices_stored = [int(i) for i in sales_prices_stored]

    print(sales_prices_stored)
    new_sales = []

    #If individual_sales is not the same lenght as sales then there is a new sale, add that sale to the database
    if len(individual_sales) != len(sales):
        #Find the difference between the two arrays
        difference = [i for i in individual_sales + sales if i not in individual_sales or i not in sales]
        #Print the difference
        print(difference)
        #Update the previous_individual_sales
        collection.update_one({"_id": 1}, {"$set": {"sales": individual_sales}})
        #set new_sales to the difference price
        new_sales = [i["price"] for i in difference]
        #Turn the new_sales into ints
        new_sales = [int(i) for i in new_sales]
        print(new_sales)
    elif len(individual_sales) == len(sales):
        print("No new sales detected")  

    #######################################Update Storage#############################################
    #Find all the entries in the storage db with amount greater than 0
    storage_stock = storage.find({"amount": {"$gt": 0}})
    for i in storage_stock:
        #Look to see if there is a match from the sales_prices_stored array and the storage_entries "sold_price" values, if there is, print text giving details.
        for j in new_sales:
            print(j)
            if j == i["sold_price"]:
                profit = (i["sold_price"] * 0.85) - i["buy_price"]
                print("Sold " + i["name"] + " for " + str(i["sold_price"]) + " and made a profit of " + str(profit) + " DKK after commission")
                #If there is a match then subtract the amount by the sales_amount and update the storage and add a entry to the sold collection, get the time from the individual_sales array, also get the amount from the sales_amounts array
                storage.update_one({"_id": i["_id"]}, {"$set": {"amount": i["amount"] - sales_amounts[sales_prices_stored.index(j)]}})
                sold_storage.insert_one({"name": i["name"], "buy_price": i["buy_price"], "sold_price": i["sold_price"], "profit": profit, "image": i["image"], "time": individual_sales[sales_prices_stored.index(j)]["time"], "amount": sales_amounts[sales_prices_stored.index(j)]})
                break
            else:
                continue
        else:
            continue
        break