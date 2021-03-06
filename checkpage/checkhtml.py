# This application will check whether the page contains any HTML elements
# that contain the search term located in the environment variable file
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
hm = True
# Chrome webdriver SSL disabling options
options = webdriver.ChromeOptions()
options.add_argument('--ignore-ssl-errors=yes')
options.add_argument('--ignore-certificate-errors')

# if hm == True:
# options.add_argument('--headless')  
# options.add_argument('--disable-gpu')

# Browser variable setting the browser driver
# downloaded & installed via webdriver manager
browser = webdriver.Chrome(ChromeDriverManager().install())

def checkforterm(records,search_term):
    data = []
    
    for record in records:
        
        record_id = record['recordid']
        record_coname = record['coname']
        record_joburl = record['jobsurl']
        
        result = {
            'recordid': record_id,
            'coname': record_coname,
            'jobsurl': record_joburl,
            'searchcount': '',
            'searchfound' : ''
        }

        browser.get(record_joburl)
        time.sleep(1)
        elements = browser.find_elements_by_xpath(
            '//*[text()[contains(., "%s")]]' % search_term)

        if not elements:
            print('Jobs page for co.', record_coname, 
                    'No HTML element(s) containing the text', 
                    '"'+search_term+'"', 'found.')
            result['searchcount'] = 0
            result['searchfound'] = False
        else:
            print('Jobs page for co.', record_coname,
                str(len(elements)), 'HTML elements containing the text',
                '"'+search_term+'"', 'found.')
            result['searchcount'] = len(elements)
            result['searchfound'] = True
        data.append(result)
    print('Selenium headless Chrome browser now closing.')
    browser.quit()
    return data
    
    
