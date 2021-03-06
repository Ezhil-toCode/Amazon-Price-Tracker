import requests #pip install requests
from bs4 import BeautifulSoup #pip install bs4
import pygame #pip install  pygame
import pync #pip install pync
import os
import time
import json

with open('settings.json','r') as file:
    settings_list = json.load(file)

# initializing notify2
# notify2.init("Amazon Price Tracker")

# To play a ding if the product is in our budget 
pygame.mixer.init()
pygame.mixer.music.load("ding.wav")

# initializing Currency Symbols to substract it from our string
currency_symbols = ['€', '	£', '$', "¥", "HK$", "₹", "¥", "," ] 

# the URL we are going to use


# Google "My User Agent" And Replace It
headers = {"User-Agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36'} 

def checking_price():
    for settings in settings_list:
        if settings.get('goal_reached'):
            continue

        # Set your budget
        my_price = settings['budget']
        URL = settings['url']

        page = requests.get(URL, headers=headers)
        soup  = BeautifulSoup(page.content, 'html.parser')

        #Finding the elements
        product_title = soup.find(id= "productTitle").get_text()
        product_price_block = soup.find(id= "priceblock_ourprice")
        if product_price_block:
            product_price = product_price_block.get_text()
        else:
            print("Could not find price for "+product_title.strip())
            continue

        # using replace() to remove currency symbols
        for i in currency_symbols : 
            product_price = product_price.replace(i, '')

        #Converting the string to integer
        product_price = int(float(product_price))


        print("The Product Name is:" ,product_title.strip())
        print("The Price is:" ,product_price)

        # Making Alert
        # alert = notify2.Notification(product_title.strip(),message=f'Current Price: {product_price}', icon='')
        # alert.set_urgency(notify2.URGENCY_NORMAL)
        # alert.show()
        pync.notify(f'Current Price: {product_price}', title=product_title.strip(), open=URL)

        # checking the price
        if(product_price<my_price):
            settings['goal_reached'] = True
            pygame.mixer.music.play()
            print("You Can Buy This Now!")
            time.sleep(3) # audio will be played first then exit the program. This time for audio playing.
            # exit()
        else:
            print("The Price Is Too High!")

while True:
    checking_price()
    time.sleep(3600) #It is set to run the program once in an hour! You can change by changing the value in seconds!
