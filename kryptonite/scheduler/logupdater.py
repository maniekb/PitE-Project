import calendar
import random
import traceback
from datetime import datetime, timedelta

from apscheduler.schedulers.background import BackgroundScheduler
from django import db

from kryptonite.algo.algo import run_algorithm
from kryptonite.dataservice.data_builder import AlgorithmDataBuilder
from kryptonite.models.models import TestScheduleLog, HistoricalResults


def start():
    _add_historic_result()
    scheduler = BackgroundScheduler()
    scheduler.add_job(_add_historic_result, 'interval', seconds=3600*24)
    scheduler.start()


def _test():
    now = datetime.now()
    random_message = "I attach random message: " + str(random.randint(1, 100))
    log = TestScheduleLog(time=now, message=random_message)
    log.save()
    db.close_old_connections()


def _add_historic_result():
    curr_date = datetime.utcnow().date()
    start_datetime = datetime(curr_date.year, curr_date.month, curr_date.day, 0, 0, 0, 0) - timedelta(days=1)
    end_datetime = datetime(curr_date.year, curr_date.month, curr_date.day, 23, 59, 0, 0) - timedelta(days=1)
    if HistoricalResults.objects.filter(time__year=start_datetime.year, time__month=start_datetime.month,
                                        time__day=start_datetime.day).exists():
        log = TestScheduleLog(time=datetime.now(),
                              message="Record for day {} already exists".format(start_datetime.date()))
        log.save()
        db.close_old_connections()
        return
    start = calendar.timegm(start_datetime.utctimetuple())
    end = calendar.timegm(end_datetime.utctimetuple())
    start_currency = "BTC"
    amount = 1.0
    include_margin = True
    data_builder = AlgorithmDataBuilder()
    data = data_builder.get_data(start, end)
    try:
        result = run_algorithm(data, start_currency, float(amount), include_margin)
    except Exception as err:
        mess = "Crash in algorithm!!!\n{}".format(traceback.format_exc())
        print(mess)
        log = TestScheduleLog(time=datetime.now(), message=mess)
        log.save()
        result = {}
    if result:
        his_res = HistoricalResults(time=datetime.strptime(result["time"], "%d/%m/%Y %H:%M:%S"), results=result)
        his_res.save()
    else:
        log = TestScheduleLog(time=datetime.now(), message="Didn't find any result to add to database")
        log.save()
