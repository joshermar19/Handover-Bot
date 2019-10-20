from jira.client import JIRA
from settings import *


session = JIRA(ATLASSIAN_URL, basic_auth=(JIRA_USER, JIRA_KEY))


def create_issue(description, date_local):
    """Expects one argument to be used for the description field.
    Will return an issue object once the issue has posted to Jira.
    """

    issue_fields = {
        'project': JIRA_PROJECT,
        'summary': f'NOC Handover {date_local}',
        'description': description,
        'issuetype': {'name': 'Story'},
    }

    handover_issue = session.create_issue(fields=issue_fields)

    return handover_issue
