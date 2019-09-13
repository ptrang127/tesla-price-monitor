from datetime import date
from bs4 import BeautifulSoup
from selenium import webdriver

import json
import os
import smtplib

# function used to send email to yourself
def send_mail(email_body):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('username@domain.com', "password") # replace these fields with your email username and password

    subject = "Tesla Price Notification!"

    msg = f"Subject: {subject}\n\n{email_body}"
    
    server.sendmail(
        'username@domain.com', # from
        'username@domain.com', # to
        msg
    )

    server.quit()

# options of the webdriver
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless') # don't actually open a browser

# configure chromedriver location
current_path = os.getcwd() # get the current working directory
chromedriver_location = str(current_path) + "/chromedriver/chromedriver.exe" # locate the chromedriver
driver = webdriver.Chrome(chromedriver_location, options=options)

driver.get('https://www.tesla.com/model3/design')

page_source = driver.page_source

soup = BeautifulSoup(page_source, "html.parser")

# find all the <p> tags which specific classes (name and pricing content use these classes)
configurations = soup.find_all('p', class_="group--options_block--name text-loader--content") # find all p tags with specific class
prices = soup.find_all('p', class_="group--options_block-container_price group--options_block-option_price text-loader--content price-not-included")

email_body = ""
price_change = False # boolean to check if the price changed from the last check

for configuration, price in zip(configurations, prices):

    configuration = configuration.get_text()

    cost = price.get_text() # used in msg

    dollars = price.get_text() # get the string price ("$35,000")
    dollars = dollars.replace(",", "") # remove commas
    dollars = dollars.replace("$", "") # remove dollar sign

    current_price = int(dollars)
    
    db_file = configuration.replace(" ", "_")
    db_file = db_file.lower() + ".json"

    date = date.today() # date YYYY-MM-DD
    string_date = str(date)

    with open(db_file, 'r') as read_file:
        db = json.load(read_file)

    last_price = db['history'][-1]['price']

    if last_price > current_price:

        price_change = True
        email_body += "The " + configuration + " Model 3 has dropped in price! It is now " + cost + ". The previous price was " + "${:,}".format(last_price) + ".\n\n"

    elif last_price < current_price:

        price_change = True
        email_body += "The " + configuration + " Model 3 has increased in price! It is now " + cost + ". The previous price was " + "${:,}".format(last_price) + ".\n\n"
    
    db['history'].append({"price": current_price, "date": string_date})

    with open(db_file, 'w') as write_file:
        json.dump(db, write_file, indent=4)

# send an email if price changed
if price_change:
    email_body += "Check out the Tesla Model 3 here: https://www.tesla.com/model3"
    send_mail(email_body)

