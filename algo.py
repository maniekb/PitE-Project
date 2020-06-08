import numpy as np
import json
from itertools import permutations

data = {
    "name":[2,4,5,6]
}
print(data["name"][2])

#generate combination of triangular
def generate_combination_of_three(to_combinate):
    #tmp = [[0,1,2],[0,2,1]]
    a = [_ for _ in range(to_combinate)]
    tmp = list(permutations(a,3))
    return tmp

#returns element from "data" for "currency"
def return_specyfic_currency_from_data(data,currency):
    for currencies in data["data"]:
        if currencies["currency"] == currency:
            return currencies

#returns element in "trades" when "currency" in "data" is ffrom and "change_to" is to
def return_specyfic_currecies_in_trades(data,ffrom,to):
    currencies = return_specyfic_currency_from_data(data,ffrom)
    for trades in currencies["trades"]:
        if trades["change_to"] == to:
            return trades

#returns element from specyfic element in "trades" is data and returns elements "rate" 
def return_specyfic_record(data,record):
    return data["records"][record]["rate"]

def return_specyfic_record_date(data,record):
    return data["records"][record]["date"]


#returns value after changing 
def return_end_count(list_rates,start_value):
    val = start_value
    val *= list_rates[0]
    val /= list_rates[1]
    val *= list_rates[2]
    return val
        

#main algorithm forex = data, records - value of rates
def algorithm(forex,start_currency,start_value,records):
    tmp = len(forex["gielda"])
    combination = generate_combination_of_three(tmp)
    order_forex = []
    max_value = 0
    date = []
    for i in combination:
        value_start = start_value
        
        temporary_max = 0
        g1 = forex["gielda"][ i[0] ]
        g2 = forex["gielda"][ i[1] ]
        g3 = forex["gielda"][ i[2] ]
        
        currencies_g1 = return_specyfic_currency_from_data(g1,start_currency) 
        
        for ong1,change_to_ong1 in enumerate(currencies_g1["trades"]):
            currencies_g2 = return_specyfic_currency_from_data(g2,change_to_ong1["change_to"]) 
            
            for ong2,change_to_ong2 in enumerate(currencies_g2["trades"]):
                if change_to_ong2["change_to"] == start_currency :
                    continue
                change_to_ong3 = return_specyfic_currecies_in_trades(g3,change_to_ong2["change_to"],start_currency)
                
                for rec in range(records):
                    list_rates = []
                    list_rates.append(return_specyfic_record(change_to_ong1,rec))
                    list_rates.append(return_specyfic_record(change_to_ong2,rec))
                    list_rates.append(return_specyfic_record(change_to_ong3,rec))

                    temporary_max = return_end_count(list_rates,start_value)
                    if temporary_max >= max_value:
                        max_value = temporary_max
                        order_forex.append([g1["nazwa"],g2["nazwa"],g3["nazwa"]])
                        date.append([return_specyfic_record_date(change_to_ong1,rec)])
    return max_value,order_forex,date
                    


                
