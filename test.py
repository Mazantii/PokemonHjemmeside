from bs4 import BeautifulSoup
import requests

##Login to loppemodul.dk
url = 'https://loppemodul.dk/auth/login'
email = 'JoakimMazanti@gmail.com'
password = 'nokianokia1'

##Create a session
with requests.session() as s:
    ##Get the html from the page
    r = s.get(url).text
    html = BeautifulSoup(r, 'lxml')

    ##Get the "_token" for the session
    token = html.find('input', {"name": "_token"}).get("value")
    print(token)

    ##Create the payload
    payload = {
        '_token': token,
        'email': email,
        'password': password
    }

    ##Post the payload to the site to log in
    p = s.post(url, data=payload)

    ##Get the html from the page
    html_text = s.get('https://loppemodul.dk/b/my-sales').text
    ##Find the tbody and print it
    html = BeautifulSoup(html_text, 'lxml')
    tbody = html.find('tbody', class_="demo").text
    print(tbody)

