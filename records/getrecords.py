from airtable import Airtable

def getcleandata(apikey,base,table,view,field_coname,field_jobsurl,
    field_searchcount):

    # Load Airtable class and pass args
    airtable = Airtable(base, table, api_key=apikey)
    raw_records = airtable.get_all(view=view)
    clean_records = []

    # print(raw_records)
    for record in raw_records:
        try:
            data = {
                'recordid': record['id'],
                'coname': record['fields'][field_coname][0],
                'jobsurl': record['fields'][field_jobsurl],
                'searchcount': record['fields'][field_searchcount]
            }
            clean_records.append(data)
        except KeyError:
            print(
                'A KeyError has ocurred. Skipping record.',
                'A mapping key is empty for the record with Company Name:', 
                record['fields'][field_coname][0]+'.'
                )

    return clean_records




