from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from notifypy import Notify
from datetime import datetime
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client['amazon']
collection = db['prices']

import os



def get_data():
    options  = Options()
    #option.add_argument("--headless")
    # options.add_argument("--proxy-server=gate.nodemaven.com:8080")
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0"
    with open("product.txt") as f:
        products = f.readlines()


    driver = webdriver.Chrome(options=options)

    i = 0
    for product in products:
        driver.get(product)
        i += 1
        page_soruce = driver.page_source
        with open(f"data/{i}.html", "w", encoding="utf-8") as f:
            f.write(page_soruce)


def extract_data():
    files = os.listdir("data")
    for file in files:
        print(file)
        with open(f"data/{file}", encoding='utf-8') as f:
            content = f.read()

        soup = BeautifulSoup(content, "html.parser")
        title = soup.title.getText().split(":")[0]
        time = datetime.now()
        #print(soup.title)

        price = soup.find(class_="a-price-whole")
        priceInt = price.getText().replace(",", "").replace(".", "")
        table = soup.find(id ="productDetails_detailBullets_sections1")
        asin = table.find(class_="prodDetAttrValue").getText().strip()
        print(priceInt, asin, title, time)
        collection.insert_one({"priceInt":priceInt, "asin": asin, "title": title, "time":time})
        # with open("finaldata.txt", "a") as f:
        #     f.write(f"{priceInt}~~{asin}~~{title}~~{time}\n")

    pass



extract_data()