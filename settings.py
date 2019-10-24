from pytz import timezone
import os

TZ = timezone('America/Los_Angeles')

ATLASSIAN_URL = 'https://birdco.atlassian.net/'

JIRA_USER = os.environ.get('JIRA_USER')
JIRA_KEY = os.environ.get('JIRA_TOKEN')

JIRA_PROJECT = 'NOC'  # Use 'NP' for DEBUG

WHOOK_URL = os.environ.get('HANDOVER_WHOOK')

HIGHPR_QUERY = ('project = NOC AND created > "-36h" AND '  # CHOSE APPROPRIATE TIME!
                '(priority =  1 OR priority = 2) ORDER BY key DESC')

OUTSTD_QUERY = ('project = NOC AND type = Incident AND '
                'status != Closed AND created >= "-7d" ORDER BY key DESC')
