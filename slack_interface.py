import os
import requests
import json

WHOOK_URL = os.environ.get('HANDOVER_WHOOK')


def send_handover_msg(issue):
    """Expects a valid jira issue to provide relevant info"""
    msg = (
        f'{issue.fields.summary}\n'
        f'{issue.permalink()}\n\n'
        f'{issue.fields.description}')

    slack_msg = {'text': msg}
    requests.post(WHOOK_URL, data=json.dumps(slack_msg))