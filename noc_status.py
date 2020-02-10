from flask import Flask, jsonify, request
import hashlib
import slack
import hmac
import os


OAUTH_TOKEN = os.environ['SLACK_DEV_TOKEN']
SIGN_SECRET = os.environ['SLACK_SIGN_SECRET'].encode('ascii')  # MUST BE ASCII ¯\_(ツ)_/¯
AUTHORIZED_USERS = ['joshermar']

VIEW = {
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
    "blocks": [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "This is a mrkdwn section block :ghost: *this is bold*, and ~this is crossed out~, and <https://google.com|this is a link>"
            }
        }
    ]
}


client = slack.WebClient(token=OAUTH_TOKEN)

app = Flask(__name__)


def _verify_signature(request):
    body = request.get_data().decode('utf-8')
    timestamp = request.headers['X-Slack-Request-Timestamp']

    base = f'v0:{timestamp}:{body}'.encode('utf-8')  # Apparently this needs to be ASCII
    computed_sig = f'v0={hmac.new(SIGN_SECRET, base, digestmod=hashlib.sha256).hexdigest()}'

    # # DEBUG
    # print(computed_sig)
    # print(request.headers['X-Slack-Signature'])

    return computed_sig == request.headers['X-Slack-Signature']


@app.route('/issues', methods=['POST'])
def issues():

    # Check for correct signing secret
    if not _verify_signature(request):
        return 'Invalid secret!'

    # Check for user authorization
    user_name = request.form['user_name']
    if user_name not in AUTHORIZED_USERS:
        return jsonify({'text': f'User {user_name} is not authorized to do that ;('})

    tid = request.form['trigger_id']
    print('Using tid: ', tid)

    client.views_open(trigger_id=request.form['trigger_id'], view=VIEW)

    # This only happens if above checks do not fail
    return jsonify({'text': 'Returned'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

