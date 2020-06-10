from datetime import datetime
from itertools import permutations


def run_algorithm(data, start_symbol, amount):
    number = len(data.__dict__()["gielda"][0]["data"][0]["trades"][0]["records"])
    result = algorithm(data.__dict__(), start_symbol, amount, number)
    if result:
        result["time"] = datetime.fromtimestamp(result["time"] / 1000 - 7200)
    return result


# main algorithm forex = data, records - number of rates
def algorithm(forex, start_currency, start_value, records):
    tmp = len(forex["gielda"])
    combination = generate_combination_of_three(tmp)
    max_value = 0
    result = {}
    for i in combination:
        value_start = start_value

        temporary_max = 0
        g1 = forex["gielda"][i[0]]
        g2 = forex["gielda"][i[1]]
        g3 = forex["gielda"][i[2]]

        currencies_g1 = return_specific_currency_from_data(g1, start_currency)
        if currencies_g1 is None:
            continue
        for ong1, change_to_ong1 in enumerate(currencies_g1["trades"]):
            currencies_g2 = return_specific_currency_from_data(g2, change_to_ong1["change_to"])
            if currencies_g2 is None:
                continue
            for ong2, change_to_ong2 in enumerate(currencies_g2["trades"]):
                if change_to_ong2["change_to"] == start_currency:
                    continue
                change_to_ong3 = return_specific_currencies_in_trades(g3, change_to_ong2["change_to"], start_currency)
                if change_to_ong3 is None:
                    continue

                for rec in range(records):
                    list_rates = [return_specific_record(change_to_ong1, rec),
                                  return_specific_record(change_to_ong2, rec),
                                  return_specific_record(change_to_ong3, rec)]
                    if None in list_rates:
                        continue
                    temporary_max = return_end_count(list_rates, start_value)
                    if temporary_max >= max_value:
                        max_value = temporary_max

                        result = {
                            "start_currency": start_currency,
                            "start_value": start_value,
                            "value": max_value,
                            "exchanges": [g1["nazwa"], g2["nazwa"], g3["nazwa"]],
                            "currencies": [change_to_ong1["change_to"],
                                           change_to_ong2["change_to"],
                                           change_to_ong3["change_to"]],
                            "rates": list_rates,
                            "time": return_specific_record_date(change_to_ong1, rec)
                        }

    return result


# generate combination of triangular
def generate_combination_of_three(to_combinate):
    a = [_ for _ in range(to_combinate)]
    tmp = list(permutations(a, 3))
    return tmp


# returns element from "data" for "currency"
def return_specific_currency_from_data(data, currency):
    for currencies in data["data"]:
        if currencies["currency"] == currency:
            return currencies


# returns element in "trades" when "currency" in "data" is ffrom and "change_to" is to
def return_specific_currencies_in_trades(data, ffrom, to):
    currencies = return_specific_currency_from_data(data, ffrom)
    if currencies is None:
        return None
    for trades in currencies["trades"]:
        if trades["change_to"] == to:
            return trades


# returns element from specyfic element in "trades" is data and returns elements "rate"
def return_specific_record(data, record):
    if data["records"]:
        return data["records"][record]["rate"]
    else:
        return None


# returns value after changing
def return_end_count(list_rates, start_value):
    val = start_value
    val *= list_rates[0]
    val *= list_rates[1]
    val *= list_rates[2]
    return val


def return_specific_record_date(data, record):
    return data["records"][record]["date"]
