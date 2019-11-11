import requests
import json
from settings import WHOOK_URL


def _txt_block(text):
    return {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": text
        }
    }


def _section_builder(section):
    """Will return a list of properly formatted issue blocks or a list containing a single no issue msg block"""

    def issue_block(issue):
        """Get relevant fields from issue and return a nicely formatted block"""
        assignee = getattr(issue.fields.assignee, 'name', 'unassigned')
        created = issue.fields.created
        block = _txt_block(
            f'<{issue.permalink()}|*{issue.key} — {assignee} — created {created[:10]}_{created[11:16]}*>\n'
            f'{issue.fields.summary[:70]}\n'
            '\n')
        return block

    blocks = [
        {"type": "divider"},  # This provides a nice line which delimits sections
        _txt_block(section['heading'])]

    # Quite simply, if there are issues, show them. Othrwise, show the "no issues message"
    if section['issues']:
        issue_blocks = [issue_block(issue) for issue in section['issues']]
        blocks.extend(issue_blocks)
    else:
        no_issues_msg = _txt_block(section['no_issues_msg'])
        blocks.append(no_issues_msg)

    return blocks


def send_handover_msg(sections, handover_issue):
    title = _txt_block(f'<{handover_issue.permalink()}|*{handover_issue.fields.summary}*>')

    blocks = [_txt_block('@here'), title]

    for section in sections:
        sec_blocks = _section_builder(section)
        blocks.extend(sec_blocks)

    slack_msg = {"blocks": blocks}

    requests.post(WHOOK_URL, data=json.dumps(slack_msg))


def send_reminder_msg():
    reminder_text = (
        '@here\n'
        '\n'
        '*Comence handover standup.*\n'
        '_Please close the handover issue once the handover process is complete._\n')

    slack_msg = {"blocks": [_txt_block(reminder_text)]}

    requests.post(WHOOK_URL, data=json.dumps(slack_msg))
