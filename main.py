# main.py

# Import all used modules
import http.client, urllib, urllib.request
import os, sys
from dotenv import load_dotenv

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

pushNotification('TEST')

# -------- END Main Body --------