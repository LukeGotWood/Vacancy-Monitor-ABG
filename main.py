# main.py

# Import all used modules
import http.client, urllib, urllib.request
import os, sys
from dotenv import load_dotenv
from selenium import webdriver

# Check for .env
if not os.path.isfile(os.path.join(os.path.dirname(os.path.realpath(__file__)), '.env')):
    print('No .env file found...\nExiting...')
    sys.exit(1)

# Load enviromental variables
load_dotenv()
TOKENKEY = os.getenv('TOKENKEY')
USERKEY = os.getenv('USERKEY')

# Declare functions
def pushNotification(msg):
    conn = http.client.HTTPSConnection('api.pushover.net:443')
    conn.request(
        'POST',
        '/1/messages.json',
        urllib.parse.urlencode({
            'token': TOKENKEY,
            'user': USERKEY,
            'message': msg
        }),
        { 'Content-type': 'application/x-www-form-urlencoded' }
    )
    conn.getresponse()

# -------- Main Body --------

# Set chrome to be headless to not launch window
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36')

# Set chrome as the webdriver
driver = webdriver.Chrome(options=options)

# Load the required SU page
driver.get('https://www.astonsu.com/housing/abg/abg_vacancies/')

# Check the correct page has been loaded
assert 'Current Vacancies' in driver.title

# Using XPATH, get the correct <p> tag
elem = driver.find_element_by_xpath('/html/body/form/div[4]/div/div[2]/section[3]/div/p[10]')

elems = driver.find_elements_by_xpath('/html/body/form/div[4]/div/div[2]/section[3]/div/p[10]')

if len(elems) == 1:
    elem = elems[0]

    # if the text is anything other than expected or <p> tag doesnt exist, send notification
    if str(elem.text) != 'There are none currently avalalble.\n ':
        pushNotification(elem.text)
else:
    pushNotification('Possible vacancy')

# Close the driver
driver.close()

# End the Program
sys.exit(0)

# -------- END Main Body --------