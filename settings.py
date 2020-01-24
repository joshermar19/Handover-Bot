from pytz import timezone
import os

# Jira Secrets
JIRA_USER = os.environ.get('JIRA_USER')
JIRA_KEY = os.environ.get('JIRA_TOKEN')

# Jira specific settings
JIRA_URL = 'https://birdco.atlassian.net/'
JIRA_PROJECT = 'NOC'  # Use 'NP' for debug, 'NOC' for production

# Slack Secrets
SLACK_WHOOK = os.environ.get('HANDOVER_WHOOK')
SLACK_TOKEN = os.environ.get('SLACK_TOKEN')

# Slack channel prefix
CHN_URL_BASE = 'https://birdrides.slack.com/archives/'

# Other settings
TZ = timezone('America/Los_Angeles')
JIRA_SEP = '—' * 35 + '\n\n'
MAX_SUM_LEN = 70

# Macros for queries
_BASE = 'project = NOC'
_SORT = 'ORDER BY key DESC'
_ISS_TYPES = '(type = Incident or type = "Platform Partner Outage")'

# JQL queries used to populate issue sections
HO_QUERY = f'{_BASE} AND type = Story AND summary ~ "NOC Handover" AND status != Done {_SORT}'
CR_QUERY = f'{_BASE} AND type = "Change Record" AND created > "-24h" {_SORT}'
P1_QUERY = f'{_BASE} AND {_ISS_TYPES} AND priority = 1 AND created > "-36h" {_SORT}'
P2_QUERY = f'{_BASE} AND {_ISS_TYPES} AND priority = 2 AND status != Closed {_SORT}'
P3_QUERY = f'{_BASE} AND {_ISS_TYPES} AND priority = 3 AND status != Closed {_SORT}'
P4_P5_QUERY = f'{_BASE} AND {_ISS_TYPES} AND priority < 3 AND status != Closed {_SORT}'
