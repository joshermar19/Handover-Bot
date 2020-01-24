from jira_interface import create_ticket, update_ticket
from slack_interface import send_msg, send_handover_msg
from settings import SECTIONS


# Fires in the middle of the work day
def mid_handover():
    pfx = "Mid-Shift"
    print(f'Commencing "{pfx}" handover job...')

    mid_ticket = create_ticket(pfx, SECTIONS)
    send_handover_msg(mid_ticket, SECTIONS)

    print('Job completed')


# Fires shortly after mid_handover
def standup_reminder():
    print('Sending "standup" reminder')
    msg = (
        '@here\n'
        '\n'
        '*Howdy! Please commence mid-shift standup.*\n'
        '_Remember to assign and close the handover ticket._\n')

    send_msg(msg)

    print('Reminder sent')


# Fires late in the evening
def on_am_handover():
    pfx = "Overnight/Morning"
    print(f'Commencing "{pfx}" handover job...')

    global on_am_ticket  # This needs to be updated by am handover

    on_am_ticket = create_ticket(pfx, SECTIONS)
    send_handover_msg(on_am_ticket, SECTIONS)

    print('Job completed')


# Fires early in the morning
def on_am_update():
    PREFACE = (
        '*Good morning team!*\n'
        '_ON/AM handover ticket has been updated to include any overnight issues._\n\n')

    print('Commencing update of ON/AM ticket')

    update_ticket(on_am_ticket, SECTIONS)

    send_handover_msg(on_am_ticket, SECTIONS, preface=PREFACE)

    print('Job completed')
