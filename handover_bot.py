from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
from pytz import timezone
import jira_interface
import slack_interface
from settings import *

TZ = timezone('America/Los_Angeles')

# These mesages will appear in lieu of relevant issues
NO_HIPRI_MSG = ('_No P1/P2 incidents in the past 36 hrs. Please add any other '
                'important issues that on-coming NOC techs must be made aware of._\n\n')
NO_OUTSTD_MSG = '_No outstanding issues in the past 7 days._\n\n'


def issues_text(query):
    """Only meant to be used by description text (for now)"""
    text_list = []

    issues = jira_interface.session.search_issues(query)

    for issue in issues:
        assignee = getattr(issue.fields.assignee, 'name', 'unassigned')
        cre = issue.fields.created

        text_list.append(
            f'*{issue.key} — {assignee} — created {cre[:10]}_{cre[11:16]}*\n'
            f'{issue.permalink()}\n'
            f'{issue.fields.summary[:66]}\n'
            '\n')

    return ''.join(text_list)


def description_text(date_local):
    """This function returns all of the relevant description text properly formatted"""
    highpri_issus = issues_text(HIGHPR_QUERY) or NO_HIPRI_MSG
    outstd_issues = issues_text(OUTSTD_QUERY) or NO_OUTSTD_MSG

    description_items = [  # Assembles all the different pieces of description field
        '*Major Incidents (-36 hrs)*:\n',
        '\n',
        highpri_issus,
        '*Outstanding Issues (-7 days)*:\n',
        '\n',
        outstd_issues
    ]

    return ''.join(description_items)


def handover_job():
    date_local = datetime.now(TZ).date()

    description = description_text(date_local)
    issue = jira_interface.create_issue(description, date_local)

    slack_interface.send_handover_msg(issue)


def main():
    sched = BlockingScheduler()
    sched.add_job(handover_job, 'cron', hour='15', timezone=TZ)
    sched.start()


if __name__ == '__main__':
    main()
