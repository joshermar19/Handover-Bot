from jira.client import JIRA
from datetime import datetime
from settings import *

session = JIRA(ATLASSIAN_URL, basic_auth=(JIRA_USER, JIRA_KEY))


def _sections_parse(sections):

    def get_issue_fields(issue):

        assignee = getattr(issue.fields.assignee, 'name', 'unassigned')
        created = issue.fields.created
        return (
            f'*{issue.key} — {assignee} — created {created[:10]}_{created[11:16]}*\n'
            f'{issue.fields.summary[:70]}\n'
            '\n')

    LINESEP = '—' * 35 + '\n\n'

    text_items = []

    for sec in sections:
        text_items.append(LINESEP)

        if sec["issues"]:
            for issue in sec["issues"]:

                issue_text = get_issue_fields(issue)
                text_items.append(issue_text)
        else:
            text_items.append(sec["no_issues_msg"])

    return ''.join(text_items)


def create_handover_issue(sections):

    date_local = datetime.now(TZ).date()

    description = _sections_parse(sections)

    issue_fields = {
        'project': JIRA_PROJECT,
        'summary': f'NOC Handover {date_local}',
        'description': description,
        'issuetype': {'name': 'Story'},
    }

    handover_issue = session.create_issue(fields=issue_fields)

    return handover_issue
