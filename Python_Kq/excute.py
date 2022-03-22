import os
import random
import time

from apscheduler.schedulers.blocking import BlockingScheduler

def job():
    os.system("/usr/bin/python3.5 autoDesk.py")

scheduler = BlockingScheduler()
scheduler.add_job(job, 'cron', hour='08', minute=str(random.randint(31, 43)))
scheduler.add_job(job, 'cron', hour='18', minute=str(random.randint(23, 37)))

scheduler.start()
