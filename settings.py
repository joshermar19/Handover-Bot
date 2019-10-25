import os

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
P2_QUERY = f'{_BASE} AND priority = 2 AND status != Closed {_SORT}'
OTHER_QUERY = f'{_BASE} AND priority < 2 AND status != Closed {_SORT}'

# These mesages will appear in lieu of relevant issues
NO_P1_TEXT = '_No outages to show for the past 36 hrs._\n\n'
NO_P2_TEXT = '_There are no outstanding P2 issues!_\n\n'
NO_OTHER_TEXT = '_There are no outstanding P3-P5 issues!_\n\n'
