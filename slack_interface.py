import requests
import json
import slack_client
from datetime import date
from settings import WHOOK_URL, CHN_PFX


def _txt_block(text):
    return {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": text
        }
    }


def _issues_section_builder(section):
    """Will return a list of properly formatted issue blocks or a list containing a single no issue msg block"""

    # Starting from scratch

    blocks = [
        {"type": "divider"},  # This provides a nice line which delimits sections
        _txt_block(section['heading'])]

    text_items = []

    # If there are not issues, this function returns early
    if not section['issues']:
        no_issues_msg = _txt_block(section['no_issues_msg'])
        blocks.append(no_issues_msg)
        return blocks

    for issue in section['issues']:
        assignee = getattr(issue.fields.assignee, 'name', 'unassigned')
        created = issue.fields.created

        text = (
            f'<{issue.permalink()}|*{issue.key} — {assignee} — {created[:10]}_{created[11:16]}*>\n'
            f'{issue.fields.summary[:70]}\n\n')

        # As long as chars do not exceed 3k, keep appending
        if len(''.join(text_items) + text) < 3000:
            text_items.append(text)

        # Once we know that any additional append would exceed 3k, finalize the current block
        # and start a new one
        else:
            channs_block = _txt_block(''.join(text_items))
            blocks.append(channs_block)

            text_items = []
            text_items.append(text)

    # This must be done for the case when text length would not have exceeded 3k
    channs_block = _txt_block(''.join(text_items))
    blocks.append(channs_block)

    return blocks


def _channels_section_builder(channs):

    blocks = [
        {"type": "divider"},
        _txt_block(f"*Open NOC Channels ({len(channs)}):*")]

    text_items = []

    for chan in channs:

        creator = slack_client.client.users_info(user=chan['creator'])
        cr_name = creator['user']['name']

        created = date.fromtimestamp(chan['created'])

        text = f"<{CHN_PFX}{chan['id']}|*#{chan['name']} — {cr_name} — {created}*>\n\n"

        # As long as chars do not exceed 3k, keep appending
        if len(''.join(text_items) + text) < 3000:
            text_items.append(text)

        # Once we know that any additional append would exceed 3k, finalize the current block
        # and start a new one
        else:
            channs_block = _txt_block(''.join(text_items))
            blocks.append(channs_block)

            text_items = []
            text_items.append(text)

    # This must be done for the case when text length would not have exceeded 3k
    channs_block = _txt_block(''.join(text_items))
    blocks.append(channs_block)

    return blocks


def send_handover_msg(handover_issue, sections, channs):
    title = _txt_block(
        '@here\n\n'
        f'<{handover_issue.permalink()}|*{handover_issue.fields.summary}*>')

    # First block is self explanatory
    blocks = [title]

    # Extend the blocks with the issues sections
    for section in sections:
        blocks.extend(_issues_section_builder(section))

    # Finally, extend the blocks with the channels section
    channs_blocks = _channels_section_builder(channs)
    blocks.extend(channs_blocks)

    slack_msg = {"blocks": blocks}

    # Debug
    print(f'Total blocks = {len(blocks)}')

    requests.post(WHOOK_URL, data=json.dumps(slack_msg))


def send_reminder_msg():
    reminder_text = (
        '@here\n'
        '\n'
        '*Commence handover standup.*\n'
        '_Please close the handover issue once the handover process is complete._\n')

    slack_msg = {"blocks": [_txt_block(reminder_text)]}

    requests.post(WHOOK_URL, data=json.dumps(slack_msg))
