"""This is not currently in use"""

import os
import slack

SLACK_TOKEN = os.environ['SLACK_TOKEN']

client = slack.WebClient(SLACK_TOKEN)
channels = client.channels_list()
