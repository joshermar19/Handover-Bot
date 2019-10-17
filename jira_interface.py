import os
from pytz import timezone
from datetime import datetime
from jira.client import JIRA

TZ = timezone('America/Los_Angeles')

URL = 'https://birdco.atlassian.net/'
USER = os.environ.get('JIRA_USER')
API_KEY = os.environ.get('JIRA_TOKEN')

session = JIRA(URL, basic_auth=(USER, API_KEY))

highpriority_query = (
    'project = NOC AND created > "-24h" AND '  # CHOSE APPROPRIATE TIME!
    '(priority =  1 OR priority = 2) '
    'ORDER BY status DESC, priority DESC, updated DESC')

outstanding_query = (
    'project = NOC AND type = Incident AND '
    'status != Closed AND created >= "-7d" ORDER BY key')


def issues_to_textlist(query):
    issues = session.search_issues(query)

    textlist = []

    for issue in issues:
        cre = issue.fields.created
        textlist.append(
            f'{issue.key} (created {cre[5:10]} {cre[11:16]})\n'
            f'{issue.fields.summary}\n')

    return textlist


def create_handover():
    date_local = datetime.now(TZ).date()

    highpri_list = issues_to_textlist(highpriority_query)
    outstd_list = issues_to_textlist(outstanding_query)

    # This list will be used to compile all of the different parts of description
    descr_items = [(
        'Daily Summary of Major Incidents, outstanding issues, and '
        'Important Change-of-Shift Notices\n\n')]

    # Major Incidents Section
    descr_items.append('*Major Incidents (-24 hrs)*:\n')
    if highpri_list:
        descr_items.extend(highpri_list)
    else:
        descr_items.append(
            '_No P1/P2 incidents in the past 24 hrs. Please add any other '
            'important issues that on-coming NOC techs must be aware of._\n\n')

    # Outstanding Issues Section
    descr_items.append(
        '\n*Outstanding Issues (-7 days)*:\n')

    if outstd_list:
        descr_items.extend(outstd_list)
    else:
        descr_items.append(
            '_No outstanding issues in the past 7 days._\n\n')

    # Important Notes Section
    descr_items.append(
        '\n*Important Notes*:\n_Please add any relevant '
        'notes regarding incidents or other important issues._')

    # That concludes the composing of the list of text items.
    descr = ''.join(descr_items)

    issue_fields = {
        'project': 'NOC',
        'summary': f'NOC Handover {date_local}',
        'description': descr,
        'issuetype': {'name': 'Story'},
    }

    handover_issue = session.create_issue(fields=issue_fields)

    return handover_issue
