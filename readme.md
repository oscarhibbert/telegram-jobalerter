# Job Alerter App

A headless application written in Python that regularly monitors for new job vacancies added to a company’s careers page based on a specific search term. 

Company careers page URLs to monitor are managed in Airtable & checked by the application.

The application then sends an alert for any new vacancies to a private Telegram channel when detected.

## Installation

This application is tested with Python 3.7.

1. Using git ``` $ git clone https://github.com/oscarhibbert/jobalerter-app```

2. Navigate to the app directory ```$ cd jobalerter-app```

3. Install all dependencies using pipenv ```$ cd pipenv install```


## Configuration

1. Create a free Airtable account [here](https://airtable.com/signup).

2. Create a new Airtable base, table & view. See [here](https://support.airtable.com/hc/en-us/articles/360021518753-Getting-started-starting-with-the-base-ics). * See below for field information. **Special attention to search count field**.

3. Create a Telegram bot. See [here](https://sarafian.github.io/low-code/2020/03/24/create-private-telegram-chatbot.html). * No need to read further than 'disable joining groups'.

4. Create an environment variable ```.env``` file in the application directory with the following config:

```
# 1. Airtable connection & base configuration
AIRTABLE_APIKEY = ''
AIRTABLE_BASE = ''
AIRTABLE_TABLE = ''
AIRTABLE_VIEW = ''

# Airtable record configuration
# The Airtable field containing the company name
AIRTABLE_FIELD_CO_NAME = ''

# The Airtable field containing the job page URL
AIRTABLE_FIELD_CO_JOBPAGE_URL = ''

# The Airtable field containing the search count no.
# Field must be a 'number' set to 'integer' & be prefilled with the number '0'
# if search count field is not prefilled with '0' for the record it will be skipped
AIRTABLE_FIELD_SEARCH_COUNT = ''


# 2. Telegram configuration
TELEGRAM_APIKEY = ''
TELEGRAM_CHATID = ''


# 3. Xpath configuration
# the xpath selector to look for the search term
# xpath must include the s% operator which will replace 
# with SEARCH_TERM when the application runs e.g.
# '//*[text()[contains(.,"%s")]]'
XPATH_SELECTOR = ''

# Search term for xpath locator
SEARCH_TERM = ''
```


## Run the Application

From the app directory ```$ pipenv run python3 jobchecker.py```


## Limitations

* No handling for career pages which have CAPATCHA walls.

* Currently limited to monitoring a maximum of ten Airtable records.


## Final Note

This app works great when run in the background by [launchd](https://www.launchd.info/) the process used by MacOS to manage  daemons and agents.

