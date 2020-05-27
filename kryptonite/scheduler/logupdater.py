from datetime import datetime
import random
from apscheduler.schedulers.background import BackgroundScheduler
from kryptonite.models.models import TestScheduleLog


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(_test, 'interval', seconds=60)
    scheduler.start()


def _test():
    now = datetime.now()
    random_message = "I attach random message: " + str(random.randint(1, 100))
    log = TestScheduleLog(time=now, message=random_message)
    log.save()
