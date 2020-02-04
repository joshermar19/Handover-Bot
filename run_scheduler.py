from apscheduler.schedulers.blocking import BlockingScheduler
from settings import TZ
import jobs


def scheduler():
    sched = BlockingScheduler()

    sched.add_job(
        jobs.mid_handover, 'cron', hour='14', minute='30', timezone=TZ)

    sched.add_job(
        jobs.standup_reminder, 'cron', hour='15', timezone=TZ)

    sched.add_job(
        jobs.on_am_handover, 'cron', hour='23', minute='30', timezone=TZ)

    sched.add_job(
        jobs.on_am_update, 'cron', hour='05', minute='30', timezone=TZ)

    print('Starting jobs scheduler...\n')

    sched.start()


if __name__ == '__main__':
    scheduler()
