import requests

def patch(apikey,base,table,thedata):
    # Loads credentials from args
    url = 'https://api.airtable.com/v0/' + base + '/' + table
    headers = {
        'Authorization': 'Bearer ' + apikey,
        'Content-Type': 'application/json'
    }

    # Data layout for input from the compare records function in jobchecker.py
    data = {
        "records": thedata
    }

    # print('PATCH REQUEST URL \n' + str(url) + '\n')
    # print('PATCH REQUEST HEADERS \n' + str(headers) + '\n')
    print('\nPATCH REQUEST PENDING...')
    updaterecord = requests.patch(url, headers=headers, json=data)
    print('\nRESPONSE CODE\n' + str(updaterecord.status_code))
    print('\nRESPONSE JSON\n' + str(updaterecord.json()))
