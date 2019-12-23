from settings import *
from datetime import datetime
from jira.client import JIRA

SEPARATOR = '—' * 35 + '\n\n'


session = JIRA(JIRA_URL, basic_auth=(JIRA_USER, JIRA_KEY))


def get_tickets(query):
    return session.search_issues(query)


def create_ticket(pfx, sections):
    date_local = datetime.now(TZ).date()

    descr = ''.join([SEPARATOR + s.get_section() for s in sections])

    issue_fields = {
        'project': JIRA_PROJECT,
        'summary': f'{pfx} NOC Handover {date_local}',
        'description': descr,
        'issuetype': {'name': 'Story'},
    }

    ticket = session.create_issue(fields=issue_fields)
    return ticket


def update_ticket(ticket, sections):
    descr = ''.join([SEPARATOR + s.get_section() for s in sections])
    ticket.update(description=descr)
