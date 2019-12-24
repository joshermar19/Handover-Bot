from sections import full_sections
from jira_interface import create_ticket, update_ticket
from slack_interface import send_msg, send_handover_msg


# Should fire in the middle of the work day
def mid_handover():
    pfx = "Mid-Shift"
    print(f'Commencing "{pfx}" handover job...')

    sections = full_sections()
    mid_ticket = create_ticket(pfx, sections)
    send_handover_msg(mid_ticket, sections)

    print('Job completed')


# Should fire shortly after mid_handover
def standup_reminder():
    print('Sending "standup" reminder')
    msg = (
        '@here\n'
        '\n'
        '*Howdy! Please commence mid-shift standup.*\n'
        '_Remember to assign and close the handover ticket._\n')

    send_msg(msg)

    print('Reminder sent')


# Should fire late in the evening
def on_am_handover():
    pfx = "Overnight/Morning"
    print(f'Commencing "{pfx}" handover job...')
    sections = full_sections()

    global on_am_ticket  # This needs to be updated by am handover

    on_am_ticket = create_ticket(pfx, sections)
    send_handover_msg(on_am_ticket, sections)

    print('Job completed')


# Should fire early in the morning
def on_am_update():
    PREFACE = (
        '*Good morning team!*\n'
        '_ON/AM handover ticket has been updated to include any overnight issues._\n\n')

    print('Commencing update of ON/AM ticket')
    sections = full_sections()
    update_ticket(on_am_ticket, sections)

    send_handover_msg(on_am_ticket, sections, preface=PREFACE)

    print('Job completed')
