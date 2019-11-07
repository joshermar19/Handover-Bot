import os
from pytz import timezone

TZ = timezone('America/Los_Angeles')

# Where dat jira at!?
ATLASSIAN_URL = 'https://birdco.atlassian.net/'
JIRA_PROJECT = 'NP'  # Use 'NP' for debug 'NOC' for production

# Secrets
WHOOK_URL = os.environ.get('HANDOVER_WHOOK')
JIRA_USER = os.environ.get('JIRA_USER')
JIRA_KEY = os.environ.get('JIRA_TOKEN')

# For internal use as macros for queries
_BASE = 'project = NOC AND type = Incident'
_SORT = 'ORDER BY key DESC'

# JQL queries used to populate the different sections with relevant issues
P1_QUERY = f'{_BASE} AND priority = 1 AND created > "-36h" {_SORT}'
CR_QUERY = f'
P2_QUERY = f'{_BASE} AND priority = 2 AND status != Closed {_SORT}'
OT_QUERY = f'{_BASE} AND priority < 2 AND status != Closed {_SORT}'
HO_QUERY = f'
