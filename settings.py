from sections import JiraSection, SlackSection
from pytz import timezone
import os

# Just makes sense to me to have this here
TZ = timezone('America/Los_Angeles')

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
JIRA_SEP = '—' * 35 + '\n\n'
MAX_SUM_LEN = 70

# Macros for queries
_BASE = 'project = NOC'
_SORT = 'ORDER BY key DESC'
_ISS_TYPES = '(type = Incident or type = "Platform Partner Outage")'

# JQL queries used to populate issue sections
_HO_QUERY = f'{_BASE} AND type = Story AND summary ~ "NOC Handover" AND status != Done {_SORT}'
_CR_QUERY = f'{_BASE} AND type = "Change Record" AND created > "-24h" {_SORT}'
_P1_QUERY = f'{_BASE} AND {_ISS_TYPES} AND priority = 1 AND created > "-36h" {_SORT}'
_P2_QUERY = f'{_BASE} AND {_ISS_TYPES} AND priority = 2 AND status != Closed {_SORT}'
_P3_QUERY = f'{_BASE} AND {_ISS_TYPES} AND priority = 3 AND status != Closed {_SORT}'
_P4_P5_QUERY = f'{_BASE} AND {_ISS_TYPES} AND priority < 3 AND status != Closed {_SORT}'

# The following list defines the totality of sections and the order in which they will appear
SECTIONS = [
    JiraSection(
        heading='Open handover issues',
        query=_HO_QUERY,
        message_if_none='No open handover issues.',
        show_count=False
    ),
    JiraSection(
        heading='Recent change records (-24hrs, any status)',
        query=_CR_QUERY,
        message_if_none='No recent CR issues.',
        show_count=False
    ),
    JiraSection(
        heading='Recent outages (-36hrs, any status)',
        query=_P1_QUERY,
        message_if_none='No recent outages (knock on wood).',
        show_count=False
    ),
    JiraSection(
        heading='Outstanding P2 Incidents',
        query=_P2_QUERY,
        message_if_none='No outstanding P2 incidents.',
    ),
    JiraSection(
        heading='Outstanding P3 Incidents',
        query=_P3_QUERY,
        message_if_none='No outstanding P3 incidents.',
    ),
    JiraSection(
        heading='Outstanding P4-P5 Incidents',
        query=_P4_P5_QUERY,
        message_if_none='No outstanding P4-P5 incidents.',
    ),
    SlackSection(
        heading='Open NOC Channels',
    )
]
