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


""" lotta work to be done """


def issues_text(query):
    """Only meant to be used by description text (for now)"""
    text_list = []

    issues = jira_interface.session.search_issues(query)

    for issue in issues:
        assignee = getattr(issue.fields.assignee, 'name', 'unassigned')
        cre = issue.fields.created

        text_list.append(
            f'*{issue.key} — {assignee} — created {cre[:10]}_{cre[11:16]}*\n'
            f'{issue.permalink()}\n'
            f'{issue.fields.summary[:70]}\n'
            '\n')

    return text_list


def description_text(date_local):
    """This function returns all of the relevant description text properly formatted"""
    _LINESEP = '=' * 54 + '\n'

    p1_lst = issues_text(P1_QUERY)
    p2_lst = issues_text(P2_QUERY)
    other_lst = issues_text(OTHER_QUERY)

    # # Simulate queries which yield no issues
    # p1_lst = []     # Debug
    # p2_lst = []     # Debug
    # other_lst = []  # Debug

    p1_issues = ''.join(p1_lst) or NO_P1_TEXT
    p2_issues = ''.join(p2_lst) or NO_P2_TEXT
    other_issues = ''.join(other_lst) or NO_OTHER_TEXT

    # Assembles all the different pieces of description field
    description_items = [
        '*Daily Summary of major recent incidents and outstanding issues*\n',
        '\n',
        _LINESEP,
        f'*Outages in the last 36 hours:*\n',
        _LINESEP,
        '\n',
        p1_issues,
        '\n',
        _LINESEP,
        f'*Outstanding P2 Issues ({len(p2_lst)})*:\n',
        _LINESEP,
        '\n',
        p2_issues,
        '\n',
        _LINESEP,
        f'*Outstanding P3-P5 Issues ({len(other_lst)})*:\n',
        _LINESEP,
        '\n',
        other_issues,
    ]

    return ''.join(description_items)