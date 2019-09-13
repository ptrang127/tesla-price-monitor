# Tesla Model 3 Email Monitoring
A quick python script used to deliver email notifications to yourself if the Tesla Model 3 prices change. I frequently check the Tesla website for price changes because I really like Tesla's Model 3. I eventually will buy one but not anytime soon as I am broke. However, I want to be up to date with the prices.

## What is it
`tesla.py` is a very quick script I threw together to automate and notify myself of price Tesla Model 3 price changes. The script scrapes the Tesla website and pulls data from the website's contents. The script then checks the current prices of the Model 3 configurations and compares them to the most recent price. If there is a price change, the script will send an email to the target email from the specified source email.

The script then appends the current prices in a mock database in the form of  `.json` files, located in the `/db` folder. It will then use this newly appended price to check against the next time the script is run.

***

## Prerequisites
- `git`
- `python3`
    - `bs4`
    - `selenium`

***

## Setup
First, clone this project into your working machine whever you want the script to be run.

`git clone https://github.com/ptrang127/tesla_price_monitor.git`

***

### Windows
For Windows users, navigate to the `/windows` folder and locate the `tesla.py` script.

Locate the following snippets of code:

```
server.login('username@domain.com', "password")
```

and

```    
server.sendmail(
        'username@domain.com', # from
        'username@domain.com', # to
        msg
    )
```

Replace the emails with your preferred email and set your password. The script is using `gmail` as the default email protocol.

Open your `command prompt` and navigate to the `tesla_price_monitor\windows\` folder. From there, run the command:

`python tesla.py`

This command runs the script. The script checks Tesla's website and writes data into the mock datebase. If there are any changes, an email will be sent to the specified email.

If you would like to schedule this script, look into Windows Task Scheduler or Windows batch scripts.

***

## Things I learned
1. scraping dynamic content is rough