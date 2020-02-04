from pytz import timezone
import os


DEBUG = False  # "True" uses NP jira project and DEV slack whook


TZ = timezone('America/Los_Angeles')


class JiraSettings:
    USER = os.environ.get('JIRA_USER')
    TOKEN = os.environ.get('JIRA_TOKEN')

    URL = 'https://birdco.atlassian.net/'
    PROJECT = 'NP' if DEBUG else 'NOC'


class SlackSettings:
    WHOOK = os.environ.get('DEV_WHOOK') if DEBUG else os.environ.get('HANDOVER_WHOOK')

    if WHOOK == None:
        raise Exception('Missing webhook for Slack!')

    TOKEN = os.environ.get('SLACK_TOKEN')


class SectionSettings:
    MAX_SUM_LEN = 70
    CHN_URL_BASE = 'https://birdrides.slack.com/archives/'


class Queries:
    # Macros
    _BASE = 'project = NOC AND'
    _DEF_SORT = 'ORDER BY key DESC'
    _ALL_SORT = 'ORDER by priority DESC, key DESC'
    _TYPES = '(type = Incident or type = "Platform Partner Outage")'

    # JQL queries used to populate issue sections
    HO = f'{_BASE} type = Story AND summary ~ "NOC Handover" AND status != Done {_DEF_SORT}'
    CR = f'{_BASE} type = "Change Record" AND created > "-24h" {_DEF_SORT}'
    P1 = f'{_BASE} {_TYPES} AND priority = 1 AND created > "-36h" {_DEF_SORT}'
    P2 = f'{_BASE} {_TYPES} AND priority = 2 AND status != Closed {_DEF_SORT}'
    P3 = f'{_BASE} {_TYPES} AND priority = 3 AND status != Closed {_DEF_SORT}'
    P4 = f'{_BASE} {_TYPES} AND priority = 4 AND status != Closed {_DEF_SORT}'
    ALL = f'{_BASE} {_TYPES} AND status != Closed {_ALL_SORT}'


class Intervals:
    '''Followup intervals (seconds)'''
    P2 = 28800     # 4 HRS
    P3 = 86400     # 24 HRS
    P4 = 604800    # 1 Week
