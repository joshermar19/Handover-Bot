import slack
from settings import SLACK_TOKEN

client = slack.WebClient(token=SLACK_TOKEN)


def _chann_filter_append(response, chan_list):
    for chann in response['channels']:
        if not chann['is_archived'] and chann['name'][:9] == 'issue-noc':
            chan_list.append(chann)


def get_open_channels():
    channels = []

    response = client.channels_list()  # This has to be called without args the first time
    cursor = response['response_metadata']['next_cursor']

    while cursor:
        _chann_filter_append(response, channels)
        response = client.channels_list(cursor=cursor)
        cursor = response['response_metadata']['next_cursor']

    # Not sure why they're not sorted by default.. Oh well :/
    channels.sort(key=lambda chan: chan['created'])

    return channels


# We want to display the username of whoever created the channel
# Something like this should work

# client.users_profile_get(user='UE1FHRG4X')


# We also want a handy-dandy little link. We need to append the channel ID
# to the prefix: https://birdrides.slack.com/archives/
