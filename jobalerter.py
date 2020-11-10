# Load & print datetime
from datetime import datetime
print('\nJob Alerter application started @ ' + 
str(datetime.now()) + '\n')

# Load credentials & other env data
from dotenv import load_dotenv
import os

airtable_apikey = os.environ.get('AIRTABLE_APIKEY')
airtable_base = os.environ.get('AIRTABLE_BASE')
airtable_table = os.environ.get('AIRTABLE_TABLE')
airtable_view = os.environ.get('AIRTABLE_VIEW')

airtable_field_co_name = os.environ.get('AIRTABLE_FIELD_CO_NAME')
airtable_field_jobpage_url = os.environ.get('AIRTABLE_FIELD_CO_JOBPAGE_URL')
airtable_field_search_count = os.environ.get('AIRTABLE_FIELD_SEARCH_COUNT')

telegram_apikey = os.environ.get('TELEGRAM_APIKEY')
telegram_chatid = os.environ.get('TELEGRAM_CHATID')

search_term = os.environ.get('SEARCH_TERM')

# Load all modules
import checkpage.checkhtml as checkhtml
import records.getrecords as getrecords
import records.updaterecords as updaterecords
import telegram.telegrammessage as telegram

# Load compare records function.
# Takes two arguments. First is the original data, and second
# is the new data. Returns records ready for a PATCH call
def comparerecords(origdata,newdata):
    # Original data and new data
    orig_data = origdata
    new_data = newdata
    # Match records to create pairings for comparison logic
    combined_data = list(zip(orig_data, new_data))

    patch_data = []
    telegram_data = []
    
    # Comparisons and subsequent logic
    for recordpair in combined_data:

        orig_rec_id = recordpair[0]['recordid']
        co_name = recordpair[0]['coname']
        co_jobs_url = recordpair[0]['jobsurl']
        orig_rec_searchcount = recordpair[0]['searchcount']
        new_rec_searchcount = recordpair[1]['searchcount']

        # Record JSON format for each patch_data object
        record_data = {
            'id': orig_rec_id,
            'fields': {
                airtable_field_search_count: new_rec_searchcount
            }
        }

        # Record JSON format for each telegram_data object
        record_telegram_data = {
            'coname': co_name,
            'jobspage': co_jobs_url
        }

        # Instances of PM increase - 
        # Update database and notify of new listing via Telegram
        if orig_rec_searchcount < new_rec_searchcount:
            print('Search count increased for job listing page: ' + co_name)
            patch_data.append(record_data)
            telegram_data.append(record_telegram_data)

        # Instances of PM decrease - Update database only
        if orig_rec_searchcount > new_rec_searchcount:
            print('Search count decreased for job listing page: ' + co_name)
            patch_data.append(record_data)

        # Instances of PM stay the same - Do nothing
        if orig_rec_searchcount == new_rec_searchcount:
            print('Search count the same for job listing page: ' + co_name)

    return {
        'patchdata': patch_data,
        'telegramdata': telegram_data
    }


# Gets records under the base, table & view specified
# in the env file from Airtable
print('\nGetting job page URL records from Airtable...\n')
inputdata = getrecords.getcleandata(airtable_apikey, airtable_base, 
    airtable_table, airtable_view, airtable_field_co_name, 
    airtable_field_jobpage_url, airtable_field_search_count)


# Takes records pulled from Airtable as an argument
# Checks whether any HTML elements on the page
# contain the search term
# returns record including boolean True or False
# as well as a count of no. of instances appended 
# to the record
print('\nChecking each URL for no. of times', '"'+search_term+'"',
'appears and appending to each record...\n')
termcount = checkhtml.checkforterm(inputdata,search_term)


# Runs the compare records function taking the two arguments
# as above
print('\nComparing original records with new records',
      'checking initiated...\n')
recordsforpatch = comparerecords(inputdata,termcount)


# Makes a PATCH request to Airtable taking a list 
# of records as an argument
print('\nInitiating patch request...\n')
updaterecords.patch(airtable_apikey,airtable_base,
    airtable_table,
    recordsforpatch['patchdata'])


# Sends messages to specified Telegram Chat ID
# sends a message with the co name and jobs page URL
# for each co - takes the argument - companies
print('\nSending messages via Telegram...\n')
telegram.send_message(telegram_apikey,
    telegram_chatid,recordsforpatch['telegramdata'],search_term)
        
