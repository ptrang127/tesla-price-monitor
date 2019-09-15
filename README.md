# Tesla Model 3 Email Monitoring

## What is it?

A quick python script used to deliver email notifications to yourself if the Tesla Model 3 prices change. I frequently check the Tesla website for price changes because I really like Tesla's Model 3. I eventually will buy one but not anytime soon as I am broke. However, I want to be up to date with the prices.

`tesla.py` is a very quick script I threw together to automate and notify myself of price Tesla Model 3 price changes. The script scrapes the Tesla website and pulls data from the website's contents. The script then checks the current prices of the Model 3 configurations and compares them to the most recent price. If there is a price change, the script will send an email to the target email from the specified source email.

The script then appends the current prices in a mock database in the form of  `.json` files, located in the `/db` folder. It will then use this newly appended price to check against the next time the script is run. The script also uses the `logging` module to log into the `/logs` folder.

***

## Prerequisites
- `git`
- `python3`
    - `bs4`
    - `selenium`

***

## Setup
First, clone this project into your working machine or wherever you want the script to be run.

`git clone https://github.com/ptrang127/tesla_price_monitor.git`

Select the folder based on your host OS (`windows` or `raspbian`).

Locate the following snippet of code in `tesla.py`.

```
server = smtplib.SMTP('smtp.gmail.com', 587)
```
If you are not using `gmail`, look into SMTP configurations specific to your email service and change this line of code accordingly.

If you have 2-Factor Authentification enabled on your `gmail` account, which you should, you won't be able to use your actual email password. Look into creating an app password [here](https://support.google.com/accounts/answer/185833?hl=en).

***

## Usage

Open your `command prompt` or `terminal` and navigate to the appropriate folder based on your platform.

*The chromedrivers for each platform are different (Windows, Raspbian) so make sure to use the appropriate folder.*

`cd path\to\tesla_price_monitor\windows`

Then run the following command

`python tesla.py -u your_email@domain.com -p your_password -r recipient_1@domain.com recipient_2@domain.com`

This command runs the script with your email account as `your_email@domain.com`, the password to that account as `your_password`, and a list of recipients as `recipient_1@domain.com` and `recipient_2@domain.com`. Replace these fields for your specific use case. The script checks Tesla's website and writes data into the mock database. If there are any changes, an email will be sent from `your_email@domain.com` to all emails specified with the `-r` flag.

#### Windows


If you would like to schedule this script, look into Windows Task Scheduler or Windows batch scripts.

***

#### Raspbian

This script is different because Raspbian uses `chromium` instead of `google-chrome`.

If you would like to schedule this script, look into setting up a `cronjob`. For your `cronjob`, you must include `export DISPLAY =:0;` in your command as follows:

```
0 12 * * * export DISPLAY=:0; cd /path/to/tesla_price_monitor/raspberrypi && /path/to/python3 /path/to/tesla_monitor/raspberrypi/tesla.py -u your_email@domain.com -p your_password -r recipient@domain.com
```

This `cronjob` runs the script every day at 12PM.

For more help with `cronjob` scheduling, check out [Crontab Guru](https://crontab.guru/).

***

## Things I learned
1. scraping dynamic content is rough
2. debugging cronjob sucks
3. vscode is great for things other than typescript
4. argparse and flags
5. logging
6. documentation