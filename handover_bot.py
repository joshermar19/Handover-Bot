from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime

import jira_interface
import slack_interface
from settings import *




# These mesages will appear in lieu of relevant issues
NO_P1_TEXT = '_No outages to show for the past 36 hrs._\n\n'
NO_P2_TEXT = '_There are no outstanding P2 issues!_\n\n'
NO_OTHER_TEXT = '_There are no outstanding P3-P5 issues!_\n\n'



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
