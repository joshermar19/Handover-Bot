from apscheduler.schedulers.blocking import BlockingScheduler
from pytz import timezone
import jira_interface
import slack_interface

TZ = timezone('America/Los_Angeles')


def handover_job():
    handover_issue = jira_interface.create_handover()
    slack_interface.send_handover_msg(handover_issue)


def main():
    sched = BlockingScheduler()
    sched.add_job(handover_job, 'cron', hour='13', timezone=TZ)
    sched.start()


if __name__ == '__main__':
    main()
