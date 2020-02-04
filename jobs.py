import slack_interface
import jira_interface
import followup
import sections

on_am_ticket = None


# Fires in the middle of the work day
def mid_handover():
    pfx = "Mid-Shift"
    print(f'Commencing "{pfx}" handover job...')

    secs = sections.get_sections()
    mid_ticket = jira_interface.create_ticket(pfx, secs)
    slack_interface.send_handover_msg(mid_ticket, secs)

    print('Job completed')


# Fires shortly after mid_handover
def standup_reminder():
    print('Sending "standup" reminder')
    msg = (
        '@here\n'
        '\n'
        '*Howdy! Please commence mid-shift standup.*\n'
        '_Remember to assign and close the handover ticket._\n')

    slack_interface.send_msg(msg)

    print('Reminder sent')


# Fires late in the evening
def on_am_handover():
    pfx = "Overnight/Morning"
    print(f'Commencing "{pfx}" handover job...')

    global on_am_ticket  # This needs to be updated by am handover

    secs = sections.get_sections()
    on_am_ticket = jira_interface.create_ticket(pfx, secs)
    slack_interface.send_handover_msg(on_am_ticket, secs)

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

    secs = sections.get_sections()
    jira_interface.update_ticket(on_am_ticket, secs)

    slack_interface.send_handover_msg(on_am_ticket, secs, preface=PREFACE)

    print('Job completed')


def followup_reminder():
    followup_issues = followup.get_followup_issues()

    if followup_issues:
        slack_interface.send_followup_msg(followup_issues)
        print('Sent follow up message')
    else:
        print('Nothing to follow up on right now')


# I expect to use this soon
def ad_hoc_handover(pfx):
    print(f'Commencing "{pfx}" handover job...')
    secs = sections.get_sections()
    ticket = jira_interface.create_ticket(pfx, secs)
    slack_interface.send_handover_msg(ticket, secs)
    print('Job completed')
