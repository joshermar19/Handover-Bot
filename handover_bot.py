from apscheduler.schedulers.blocking import BlockingScheduler
import jira_interface
import slack_interface
from settings import *


def handover_job():
    p1_issues = jira_interface.session.search_issues(P1_QUERY)
    cr_issues = jira_interface.session.search_issues(CR_QUERY)
    p2_issues = jira_interface.session.search_issues(P2_QUERY)
    ot_issues = jira_interface.session.search_issues(OT_QUERY)
    ho_issues = jira_interface.session.search_issues(HO_QUERY)

    sections = [
        {
            "heading": f'*Outages (P1s) in the last 36 hours:*\n',
            "no_issues_msg": '_No outages to show for the last 36 hrs._\n\n',
            "issues": p1_issues
        },
        {
            "heading": f'*Deploys in the last 24 hours:*\n',
            "no_issues_msg": '_No deploys to show for the last 24 hrs._\n\n',
            "issues": cr_issues
        },
        {
            "heading": f'*Outstanding P2 Issues ({len(p2_issues)})*:\n',
            "no_issues_msg": '_There are no outstanding P2 issues!_\n\n',
            "issues": p2_issues
        },
        {
            "heading": f'*Outstanding P3-P5 Issues ({len(ot_issues)})*:\n',
            "no_issues_msg": '_There are no outstanding P3-P5 issues!_\n\n',
            "issues": ot_issues
        },
        {
            "heading": f'*Open Handover Issues ({len(ho_issues)}):*\n',
            "no_issues_msg": '_No open handover issues. Good job!_\n\n',
            "issues": ho_issues
        }]

    handover_issue = jira_interface.create_handover_issue(sections)
    slack_interface.send_handover_msg(sections, handover_issue)

    print(f'\n{handover_issue} issued and message sent!')


def main():
    sched = BlockingScheduler()
    sched.add_job(handover_job, 'cron', hour='14', minute='30', timezone=TZ)
    sched.add_job(slack_interface.send_reminder_msg, 'cron', hour='15', timezone=TZ)
    sched.start()


if __name__ == '__main__':
    main()
