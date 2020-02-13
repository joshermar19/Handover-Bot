from flask import Flask, jsonify, request
from slack_interface import client, msg_builder
from settings import NOCStatSettings
from threading import Thread
import sections
import hashlib
import hmac


INTRO_VIEW = {
    "type": "modal",
    "title": {
        "type": "plain_text",
        "text": "Open NOC Issues",
    },
    "blocks": [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "One moment while I cook that up for you..."
            }
        }
    ]
}


response = None

app = Flask(__name__)


def _verify_signature(request):
    body = request.get_data().decode('utf-8')
    timestamp = request.headers['X-Slack-Request-Timestamp']

    base = f'v0:{timestamp}:{body}'.encode('utf-8')  # Apparently this needs to be ASCII
    computed_sig = f'v0={hmac.new(NOCStatSettings.SIGN_SECRET, base, digestmod=hashlib.sha256).hexdigest()}'

    # # DEBUG
    # print(computed_sig)
    # print(request.headers['X-Slack-Signature'])

    return computed_sig == request.headers['X-Slack-Signature']


def get_ho_view():
    all_sections = sections.get_sections()
    segments = [s.get_section(for_slack=True) for s in all_sections]

    # Just a reminder, this functions returns the smallest number of preformated
    # slack "blocks" that conform to the character limit for "text" field
    blocks = msg_builder(*segments)  # Remember, each "segment" is a separate argument

    view = {
        "type": "modal",
        "title": {
            "type": "plain_text",
            "text": "Open NOC Issues",
            "emoji": True
        },
        "close": {
            "type": "plain_text",
            "text": "Close",
            "emoji": True
        },
        "blocks": blocks
    }

    return view


def initial_view(tid, view):
    global response  # A more elegant OO approach would be desireable
    response = client.views_open(trigger_id=tid, view=view)
    print('END of initial view')


def final_view():
    # This has to happen asyncronously
    vid = response.data['view']['id']  # This has to have been updated by now

    view = get_ho_view()  # Crux of the I/O bind

    client.views_update(view=view, view_id=vid)
    print('END of final view')


@app.route('/noc-status', methods=['POST'])
def noc_status():
    print('Start of Route')

    # Check for correct signing secret
    if not _verify_signature(request):
        return 'Invalid secret!'

    # Check for user authorization
    user_name = request.form['user_name']
    if user_name not in NOCStatSettings.AUTHORIZED_USERS:
        return jsonify({'text': f'User {user_name} is not authorized to do that ;('})

    initial_view(request.form['trigger_id'], INTRO_VIEW)

    # initial_view_thread = Thread(target=initial_view, args=(request.form['trigger_id'], INTRO_VIEW))
    final_view_thread = Thread(target=final_view)

    final_view_thread.start()

    print('END of Route')

    # Obviously only happens if above checks do not fail
    return ('', 200)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
