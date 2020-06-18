import json

from kryptonite.models import HistoricalResults


def get_last_week_historic_results():
    results = HistoricalResults.objects.order_by('-time')[:7]
    data = [{"time": result.time, "results": json.loads(result.results.replace("'", "\""))} for result in results]
    return data


def get_historic_result_by_date(date):
    query = HistoricalResults.objects.filter(time=date)
    if query.exists():
        result = query.first()
        return json.loads(result.results.replace("'", "\""))
