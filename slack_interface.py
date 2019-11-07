import requests
import json
from settings import *


def _section(text):
    return {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": text
        }
    }


def _parse_issues(issues):
    pass


def send_handover_msg(issue):
    pass
    # requests.post(WHOOK_URL, data=json.dumps(slack_msg))


# def PLACEHOLDER():

#     msg = (
#         '@here\n'
#         f'*{issue.fields.summary}*\n'
#         f'{issue.permalink()}\n'
#         f'{issue.fields.description}\n')

#     slack_msg = {'text': msg}