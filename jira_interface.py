import os
from pytz import timezone
from datetime import datetime
from jira.client import JIRA

TZ = timezone('America/Los_Angeles')

URL = 'https://birdco.atlassian.net/'
USER = os.environ.get('JIRA_USER')
API_KEY = os.environ.get('JIRA_TOKEN')

session = JIRA(URL, basic_auth=(USER, API_KEY))


def get_issues():
    query = (
        'project = NOC AND created > "-24h" AND '  # CHOSE APPROPRIATE TIME!
        '(priority =  1 OR priority = 2) '
        'ORDER BY status ASC, priority DESC, updated DESC')
    return session.search_issues(query)


def create_handover():
    date_local = datetime.now(TZ).date()

    issues = get_issues()

    descr_items = [(
        'Daily Summary of Major Incidents and '
        'Important Change-of-Shift Notices\n\n'
        '*Incidents*:\n')]

    if issues:
        for issue in issues:
            cre = issue.fields.created
            descr_items.append(
                f'{issue.key} (created {cre[5:10]} {cre[11:16]})\n'
                f'{issue.fields.summary}\n\n')
    else:
        descr_items.append(
            '_No P1/P2 incidents in the past 24 hrs. Please add any other '
            'important issues that on-coming NOC techs must be aware of._\n\n')

    descr_items.append(
        '*Important Notes*:\n_Please add any relevant '
        'notes regarding incidents or other important issues._')

    descr = ''.join(descr_items)

    issue_fields = {
        'project': 'NP',
        'summary': f'NOC Handover {date_local}',
        'description': descr,
        'issuetype': {'name': 'Story'},
    }

    handover_issue = session.create_issue(fields=issue_fields)

    return handover_issue
