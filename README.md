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

Replace the emails with your preferred email and set your password. The script is using `gmail` as the default email protocol. Save the file.

The chromedrivers for each platform are different (Windows, Max, Linux) use the appropriate folder.

***

### Windows
For Windows users, navigate to the `/windows` folder and locate the `tesla.py` script.

Open your `command prompt` and navigate to the `tesla_price_monitor\windows\` folder. From there, run the command:

`python tesla.py`

This command runs the script. The script checks Tesla's website and writes data into the mock datebase. If there are any changes, an email will be sent to the specified email.

If you would like to schedule this script, look into Windows Task Scheduler or Windows batch scripts.

***

### Raspbian
For Raspberry Pi users, navigate to the `/raspberrypi` folder and locate the `tesla.py` script.

Open your `terminal` and navigate to the `tesla_price_monitor\raspberrypi\` folder. From there, run the command:

`python tesla.py`

This command runs the script. The script checks Tesla's website and writes data into the mock datebase. If there are any changes, an email will be sent to the specified email. The script is different because Raspbian uses `chromium` instead of `google-chrome`.

If you would like to schedule this script, look into setting up a `cronjob`. For your `cronjob`, you must include `export DISPLAY =:0;` in your command as follows:

```
0 12 * * * export DISPLAY=:0; cd /path/to/tesla_price_monitor/raspberrypi && /path/to/python3 /path/to/tesla_monitor/raspberrypi/tesla.py
```

This `cronjob` runs the script everyday at 12PM.

For more help with `cronjob` scheduling, check out [Crontab Guru](https://crontab.guru/).

***

## Things I learned
1. scraping dynamic content is rough
2. debugging cronjob sucks