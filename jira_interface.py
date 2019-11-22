from jira.client import JIRA
from datetime import datetime, date
import slack_client
from settings import *

session = JIRA(ATLASSIAN_URL, basic_auth=(JIRA_USER, JIRA_KEY))

LINESEP = '—' * 35 + '\n\n'


def _issue_sections_parse(sections):

    def get_issue_fields(issue):
        assignee = getattr(issue.fields.assignee, 'name', 'unassigned')
        created = issue.fields.created
        return (
            f'*{issue.key} — {assignee} — {created[:10]}_{created[11:16]}*\n'
            f'{issue.fields.summary[:70]}\n'
            '\n')

    text_items = []

    for sec in sections:
        text_items.append(LINESEP)
        text_items.append(f"{sec['heading']}\n\n")

        if sec["issues"]:
            for issue in sec["issues"]:

                issue_text = get_issue_fields(issue)
                text_items.append(issue_text)
        else:
            text_items.append(sec["no_issues_msg"])

    return text_items


def _channels_parse(channs):
    text_items = [
        LINESEP,
        f"*Open NOC Channels ({len(channs)}):*\n\n"]

    for chan in channs:

        creator = slack_client.client.users_info(user=chan['creator'])
        cr_name = creator['user']['name']
        created = date.fromtimestamp(chan['created'])

        text_items.append(f"*#{chan['name']} — {cr_name} — {created}*\n")

    return text_items


def create_handover_issue(pfx, sections, channels):
    date_local = datetime.now(TZ).date()
    desc_items = _issue_sections_parse(sections) + _channels_parse(channels)

    issue_fields = {
        'project': JIRA_PROJECT,
        'summary': f'{pfx} NOC Handover {date_local}',
        'description': ''.join(desc_items),
        'issuetype': {'name': 'Story'},
    }

    handover_issue = session.create_issue(fields=issue_fields)

    return handover_issue
