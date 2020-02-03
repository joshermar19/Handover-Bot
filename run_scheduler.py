from apscheduler.schedulers.blocking import BlockingScheduler
from settings import TZ
from jobs import mid_handover, standup_reminder, on_am_handover, on_am_update


def scheduler():
    sched = BlockingScheduler()

    sched.add_job(
        mid_handover, 'cron', hour='14', minute='30', timezone=TZ)

    sched.add_job(
        standup_reminder, 'cron', hour='15', timezone=TZ)

    sched.add_job(
        on_am_handover, 'cron', hour='23', minute='30', timezone=TZ)

    sched.add_job(
        on_am_update, 'cron', hour='05', minute='30', timezone=TZ)

    print('Starting jobs scheduler...\n')

    sched.start()


if __name__ == '__main__':
    scheduler()
