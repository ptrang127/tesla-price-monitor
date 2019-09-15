from datetime import date
from bs4 import BeautifulSoup
from selenium import webdriver

import json
import os
import smtplib
import argparse
import logging

# get command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-u', '--user', help='Username', required=True)
parser.add_argument('-p', '--password', help='Password', required=True)
parser.add_argument('-r', '--recipients', help='Recipients', nargs='+', required=True)
args = parser.parse_args()

# logger info
date = date.today() # date YYYY-MM-DD
today = str(date)
log_file = "./logs/" + today + ".log"
logging.basicConfig(filename=log_file,
                            filemode='w',
                            format='%(asctime)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)

# function used to send email(s)
def send_mail(email_body):
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    try:
        server.login(args.user, args.password)
    except:
        logging.exception('')

    subject = "Tesla Price Notification!"

    msg = f"Subject: {subject}\n\n{email_body}"
    
    for recipient in args.recipients:

        
        server.sendmail(
            args.user, # from
            recipient, # to
            msg
        )
        

    server.quit()

# options of the webdriver
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--disable-gpu')

# configure chromedriver location
current_path = os.getcwd() # get the current working directory
chromedriver_location = str(current_path) + "/chromedriver/chromedriver"
driver = webdriver.Chrome(chromedriver_location, options=options)

driver.get('https://www.tesla.com/model3/design')

page_source = driver.page_source

soup = BeautifulSoup(page_source, "html.parser")

# find all the <p> tags which specific classes (name and pricing content use these classes)
configurations = soup.find_all('p', class_="group--options_block--name text-loader--content")
prices = soup.find_all('p', class_="group--options_block-container_price group--options_block-option_price text-loader--content price-not-included")

price_change = False # boolean to check if the price changed from the last check
email_body = ""
log_message = ""
changes = []

for configuration, price in zip(configurations, prices):

    configuration = configuration.get_text()

    cost = price.get_text() # used in msg

    current_price = price.get_text() # get the string price ("$35,000")
    current_price = current_price.replace(",", "") # remove commas
    current_price = current_price.replace("$", "") # remove dollar sign

    current_price = int(current_price)
    
    db_file = configuration.replace(" ", "_")
    db_file = "./db/" + db_file.lower() + ".json"

    date = date.today() # date YYYY-MM-DD
    string_date = str(date)

    with open(db_file, 'r') as read_file:
        db = json.load(read_file)

    last_price = db['history'][-1]['price'] # most recent price (yesterday)

    if last_price > current_price:

        price_change = True
        email_body += "The " + configuration + " Model 3 has decreased in price! It is now " + cost + ". The previous price was " + cost + ".\n\n"
        changes.append(configuration + " decreased to " + cost)
        
    elif last_price < current_price:

        price_change = True
        email_body += "The " + configuration + " Model 3 has increased in price! It is now " + cost + ". The previous price was " + cost + ".\n\n"
        changes.append(configuration + " increased to " + cost)

    db['history'].append({"price": current_price, "date": string_date})

    with open(db_file, 'w') as write_file:
        json.dump(db, write_file, indent=4)

driver.quit()

logging.info("Successfully scraped Tesla website")

# send an email if price change and log
if price_change:
    email_body += "Check out the Tesla Model 3 here: https://www.tesla.com/model3"
    send_mail(email_body)
    
    for change in changes:
        logging.info(change)
else:
    logging.info("No prices changes")