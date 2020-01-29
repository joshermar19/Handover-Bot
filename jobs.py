from jira_interface import create_ticket, update_ticket
from slack_interface import send_msg, send_handover_msg
from sections import get_sections

on_am_ticket = None


# Fires in the middle of the work day
def mid_handover():
    pfx = "Mid-Shift"
    print(f'Commencing "{pfx}" handover job...')

    sections = get_sections()
    mid_ticket = create_ticket(pfx, sections)
    send_handover_msg(mid_ticket, sections)

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

    sections = get_sections()
    on_am_ticket = create_ticket(pfx, sections)
    send_handover_msg(on_am_ticket, sections)

    print('Job completed')


# Fires early in the morning
def on_am_update():
    # Just in case this fires before overnight ticket exists
    if not on_am_ticket:
        return

    PREFACE = (
        '*Good morning team!*\n'
        '_ON/AM handover ticket has been updated to include any overnight issues._\n\n')

    print('Commencing update of ON/AM ticket')

    sections = get_sections()
    update_ticket(on_am_ticket, sections)

    send_handover_msg(on_am_ticket, sections, preface=PREFACE)

    print('Job completed')


# I expect to use this soon
def ad_hoc_handover(pfx):
    print(f'Commencing "{pfx}" handover job...')
    sections = get_sections()
    ticket = create_ticket(pfx, sections)
    send_handover_msg(ticket, sections)
    print('Job completed')
