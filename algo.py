import numpy as np
import json


data = {
    "name":[2,4,5,6]
}
print(data["name"][2])

#generate combination of triangular
def generateCombinationOfThree(tocombinate):
    tmp = [[0,1,2],[0,2,1]]
    return tmp

#returns element from "data" for "currency"
def returnSpecyficCurrencyFromData(data,currency):
    for currencies in data["data"]:
        if currencies["currency"] == currency:
            return currencies

#returns element in "trades" when "currency" in "data" is ffrom and "change_to" is to
def returnSpecyficCurrenciesInTrades(data,ffrom,to):
    currencies = returnSpecyficCurrencyFromData(data,ffrom)
    for trades in currencies["trades"]:
        if trades["change_to"] == to:
            return trades

#returns element from specyfic element in "trades" is data and returns elements "rate" 
def returnSpecyficRecord(data,record):
    return data["records"][record]["rate"]

#returns value after changing 
def returnEndCount(list_rates,start_value):
    val = start_value
    val *= list_rates[0]
    val /= list_rates[1]
    val *= list_rates[2]
    return val
        

#main algorithm
def algorithm(forex,start_currency,start_value,records):
    tmp = len(forex["gielda"])
    combination = generateCombinationOfThree(tmp)

    for i in combination:
        valuestart = start_value
        max_value = 0
        temporary_max = 0
        g1 = forex["gielda"][ i[0] ]
        g2 = forex["gielda"][ i[1] ]
        g3 = forex["gielda"][ i[2] ]
        
        currenciesg1 = returnSpecyficCurrencyFromData(g1,start_currency) 
        
        for ong1,change_to_ong1 in enumerate(currenciesg1["trades"]):
            currenciesg2 = returnSpecyficCurrencyFromData(g2,change_to_ong1["change_to"]) 
            
            for ong2,change_to_ong2 in enumerate(currenciesg2["trades"]):
                if change_to_ong2["change_to"] == start_currency :
                    continue
                change_to_ong3 = returnSpecyficCurrenciesInTrades(g3,change_to_ong2["change_to"],start_currency)
                
                for rec in range(records):
                    list_rates = []
                    list_rates.append(returnSpecyficRecord(change_to_ong1,rec))
                    list_rates.append(returnSpecyficRecord(change_to_ong2,rec))
                    list_rates.append(returnSpecyficRecord(change_to_ong3,rec))

                    temporary_max = returnEndCount(list_rates,start_value)
                    max_value = max(temporary_max,max_value)

                    


                
