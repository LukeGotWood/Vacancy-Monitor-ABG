# main.py

# Import all used modules
import http.client, urllib, urllib.request, socket
import os, sys, time
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
NETWORKWAIT = os.getenv('NETWORKWAIT')

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

def is_network():
    hostname = "one.one.one.one"
    try:
        # see if we can resolve the host name -- tells us if there is
        # a DNS listening
        host = socket.gethostbyname(hostname)
        # connect to the host -- tells us if the host is actually
        # reachable
        s = socket.create_connection((host, 80), 2)
        s.close()
        return True
    except:
        pass
        return False

# -------- Main Body --------

# Wait until network connection is established before continuing
while not is_network():
    print(f'No network detected, waiting for { NETWORKWAIT } seconds...')
    time.sleep(NETWORKWAIT)

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

    print(f'Element text: { repr(elem.text) }')

    # if the text is anything other than expected or <p> tag doesnt exist, send notification
    if str(elem.text) != 'There are none currently avalalble.\n ':
        print('Text has changed, send notification')
        pushNotification(repr(elem.text))
else:
    print('Element not found, possible vacancy')
    pushNotification('Possible vacancy')

# Close the driver
driver.close()

print('DONE')

# End the Program
sys.exit(0)

# -------- END Main Body --------