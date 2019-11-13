import slack
from settings import SLACK_TOKEN

client = slack.WebClient(token=SLACK_TOKEN)


def get_open_channels():

    def chann_filter_append(response, l):
        for chann in response['channels']:
            if not chann['is_archived'] and chann['name'][:9] == 'issue-noc':
                l.append(chann)

    channels = []

    response = client.channels_list()  # This has to be called without args the first time
    chann_filter_append(response, channels)
    cursor = response['response_metadata']['next_cursor']

    while cursor:
        response = client.channels_list(cursor=cursor)
        chann_filter_append(response, channels)
        cursor = response['response_metadata']['next_cursor']

    # Not sure why they're not sorted by default.. Oh well :/
    channels.sort(key=lambda chan: chan['created'], reverse=True)

    return channels
