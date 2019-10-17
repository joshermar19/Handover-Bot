'''
# The bassic flow seems to be:

import hvac
import os


client = hvac.Client(url=os.environ.get('VAULT_ADDR'))

client.token = ''  # Strangely not necessary for me :/

read_response = client.read('path/to/secret')
'''
