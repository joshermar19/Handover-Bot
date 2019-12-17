from apscheduler.schedulers.blocking import BlockingScheduler
import jira_interface
import slack_interface
import slack_client
from settings import *


def handover_job(pfx):
    p2_issues = jira_interface.session.search_issues(P2_QUERY)
    ot_issues = jira_interface.session.search_issues(OT_QUERY)

    sections = [
        {
            "heading": f'*Open Handover Issues:*',
            "no_issues_msg": '_No open handover issues._\n\n',
            "issues": jira_interface.session.search_issues(HO_QUERY)
        },
        {
            "heading": f'*Outages in the last 36 hours:*',
            "no_issues_msg": '_No outages in last 36 hrs (knock on wood)._\n\n',
            "issues": jira_interface.session.search_issues(P1_QUERY)
        },
        {
            "heading": f'*Deploys in the last 24 hours:*',
            "no_issues_msg": '_No recent deploys._\n\n',
            "issues": jira_interface.session.search_issues(DP_QUERY)
        },
        {
            "heading": f'*Outstanding Change Requests:*',
            "no_issues_msg": '_There are no outstanding CR issues._\n\n',
            "issues": jira_interface.session.search_issues(CR_QUERY)
        },
        {
            "heading": f'*Outstanding P2 Incidents ({len(p2_issues)}):*',
            "no_issues_msg": '_There are no outstanding P2 incidents._\n\n',
            "issues": p2_issues
        },
        {
            "heading": f'*Outstanding P3-P5 Incidents ({len(ot_issues)}):*',
            "no_issues_msg": '_There are no outstanding P3-P5 incidents._\n\n',
            "issues": ot_issues
        }]

    open_channs = slack_client.get_open_channels()

    handover_issue = jira_interface.create_handover_issue(pfx, sections, open_channs)
    slack_interface.send_handover_msg(handover_issue, sections, open_channs)

    # DEBUG
    print(f"Created: {handover_issue.permalink()}")
    print(f'Message sent!')


def main():
    sched = BlockingScheduler()

    # Morning reminder fires at 05:30
    sched.add_job(slack_interface.send_morning_reminder, 'cron', hour='05', minute='30', timezone=TZ)

    # PM Handover fires at 14:30
    sched.add_job(lambda: handover_job('PM'), 'cron', hour='14', minute='30', timezone=TZ)

    # Standup reminder fires at 15:00
    sched.add_job(slack_interface.send_standup_reminder, 'cron', hour='15', timezone=TZ)

    # AM Handover fires at 21:30. This is for On call as well as Morning Shift
    sched.add_job(lambda: handover_job('ON/AM'), 'cron', hour='21', minute='30', timezone=TZ)

    # This confirms the jobs were added
    print('Starting jobs scheduler\n')

    sched.start()


if __name__ == '__main__':
    main()
