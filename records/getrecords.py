from airtable import Airtable

def getcleandata(apikey,base,table,view):
    # Load Airtable class and pass args
    airtable = Airtable(base, table, api_key=apikey)

    # records = airtable.get_all(view='Shortlist', fields=['Startup Name','Jobs Page URL'])
    raw_records = airtable.get_all(view=view)
    clean_records = []

    # print(raw_records)
    for record in raw_records:
        try:
            data = {
                'recordid': record['id'],
                'coname': record['fields']['Startup Name (from Startups)'][0],
                'jobsurl': record['fields']['Jobs Page URL'],
                'pmtextcount': record['fields']['Product Manager Text Count']
            }
            clean_records.append(data)
        except KeyError:
            print('A KeyError has ocurred. A mapping key value is empty for',
                  'the record with Startup Name:', 
                  record['fields']['Startup Name (from Startups)'][0]+'.')

    return clean_records




