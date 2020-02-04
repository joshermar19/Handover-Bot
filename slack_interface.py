from settings import SlackSettings
import requests
import slack
import json

client = slack.WebClient(token=SlackSettings.TOKEN)


def _append_relevant(resp, rel_channs):
    # For each "resp", chech for relevant channels and append them to my list
    for c in resp['channels']:
        if c['is_archived']:
            continue
        if c['name'][:9] != 'issue-noc':
            continue
        rel_channs.append(c)


def get_open_channels():
    relevant_channels = []

    cursor = ''
    while True:  # This has to run at least once with a empty cursor
        response = client.channels_list(cursor=cursor)
        _append_relevant(response, relevant_channels)

        cursor = response['response_metadata']['next_cursor']
        if not cursor:
            break

    relevant_channels.sort(key=lambda chan: chan['created'], reverse=True)

    return relevant_channels


def get_user_name(usr):
    response = client.users_info(user=usr)
    return response['user']['name']


def _txt_block(text):
    return {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": text
        }
    }


def _block_builder(section):
    blocks = []
    block_lines = []

    for line in section.splitlines():
        # If the total char length will not exceed 3k, keep appending lines
        if len('\n'.join(block_lines)) + len(line) < 3000:
            block_lines.append(line)
        # Else reset block_lines list and append to blocks immediately
        else:
            blocks.append(_txt_block('\n'.join(block_lines)))
            block_lines = [line]

    # Append any left over lines
    if block_lines:
        blocks.append(_txt_block('\n'.join(block_lines)))

    return blocks


def send_msg(*segments):
    """Accepts any number of message segments"""
    blocks = []

    for segment in segments:
        blocks.extend(_block_builder(segment))

        if segment != segments[-1]:  # Don't add line for last (or only) segment
            blocks.append({"type": "divider"})

    msg = {"blocks": blocks}

    response = requests.post(SlackSettings.WHOOK, data=json.dumps(msg))
    print(response.status_code)


def send_handover_msg(ho_ticket, sections, preface=''):

    msg_segments = [f'@here\n{preface}<{ho_ticket.permalink()}|*{ho_ticket.fields.summary}*>']

    msg_segments.extend([s.get_section(for_slack=True) for s in sections])

    send_msg(*msg_segments)


def send_followup_msg(issues):
    msg_segments = [f'@here\nHeads up NOC team!\nPlease follow up on:\n']

    followup_items = [
        f'<{i.permalink()}|*{i.key} — P{i.fields.priority.name} — Updated: {i.fields.updated[:19]}*>'
        for i in issues
    ]

    msg_segments.extend(followup_items)

    send_msg(*msg_segments)
