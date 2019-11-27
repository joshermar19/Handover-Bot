from pytz import timezone
import os

TZ = timezone('America/Los_Angeles')

TIME_PREFIXES = ['AM', 'PM', 'ON']

# Where dat jira at!?
ATLASSIAN_URL = 'https://birdco.atlassian.net/'
JIRA_PROJECT = 'NOC'  # Use 'NP' for debug 'NOC' for production

# Secrets
WHOOK_URL = os.environ.get('HANDOVER_WHOOK')
JIRA_USER = os.environ.get('JIRA_USER')
JIRA_KEY = os.environ.get('JIRA_TOKEN')
SLACK_TOKEN = os.environ.get('SLACK_TOKEN')

# Slack channel prefix
CHN_PFX = 'https://birdrides.slack.com/archives/'

# For internal use as macros for queries
_BASE = 'project = NOC'
_SORT = 'ORDER BY key DESC'
_ISS_TYPES = '(type = Incident or type = "Platform Partner Outage")'

# JQL queries used to populate the different sections with relevant issues
HO_QUERY = f'{_BASE} AND type = Story AND summary ~ "NOC Handover" AND status != Done {_SORT}'
P1_QUERY = f'{_BASE} AND {_ISS_TYPES} AND priority = 1 AND created > "-36h" {_SORT}'
DP_QUERY = f'{_BASE} AND type = "Change Record" AND summary ~ "Deploy" AND created > "-24h" {_SORT}'
CR_QUERY = f'{_BASE} AND type = "Change Record" AND status != Closed {_SORT}'
P2_QUERY = f'{_BASE} AND {_ISS_TYPES} AND priority = 2 AND status != Closed {_SORT}'
OT_QUERY = f'{_BASE} AND {_ISS_TYPES} AND priority < 2 AND status != Closed {_SORT}'
