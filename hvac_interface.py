'''
# The bassic flow seems to be:

import hvac
import os


client = hvac.Client(url=os.environ.get('VAULT_ADDR'))

# client.token = ''

read_response = client.read('path/to/secret')
read_response['data']['jira_token']  # Etc ...

'''
