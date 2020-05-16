import numpy as np
import json


class Alg:

   

    def addToCurrencies(self,curr,toadd):
        curr["currencies"].append(toadd)

    def addElementToCurrency(self,currencies,currency,elem):
        
        for tmp in currencies["currencies"]:
            if tmp == currency :
                tmp["elements"].append(elem)

    def findPath(self,forexlist,data):
        maxincome = 0
        for tmp,f in enumerate(forexlist):
            for i,forex in enumerate(forexlist):
                if tmp == i:
                    continue


    def generate_element(self,forexname,to,day,minute,price):
        element = {
            "to": to,
            "day": day,
            "minute": minute,
            "price":price
        }
        return element
    def generate_data(self):
        
         
        
        forex = {
            "forex":[]
        }
        currencies = {
            "currencies": []
        }
        BTC = {
            "elements": []
        }
        
        ETH = {
            "elements": []
        }
        
        RIP = {
            "elements": []
        }
        self.addToCurrencies(currencies,BTC)
        self.addToCurrencies(currencies,ETH)
        self.addToCurrencies(currencies,RIP)

        tmp_price = [1,2,0.5]

        for i in range(10):
            elem = self.generate_element('a','1','USD',str(i),tmp_price[i])
            self.addElementToCurrency(currencies,BTC,elem)
            self.addElementToCurrency(currencies,ETH,elem)
            self.addElementToCurrency(currencies,RIP,elem)
            elem = self.generate_element('b','1','RIP',str(i),tmp_price[i+10])
            self.addElementToCurrency(currencies,BTC,elem)
            self.addElementToCurrency(currencies,ETH,elem)
            #self.addElementToCurrency(currencies,RIP,elem)
            elem = self.generate_element('c','1','BTC',str(i),tmp_price[i+10])
            #self.addElementToCurrency(currencies,BTC,elem)
            self.addElementToCurrency(currencies,ETH,elem)
            self.addElementToCurrency(currencies,RIP,elem)


        print(json.dumps(currencies,indent=4))
if __name__ == "__main__":
    algo = Alg()
    algo.generate_data()


data = {
    "name":[2,4,5,6]
}
print(data["name"][2])

def generateCombinationOfThree(tocombinate):
    tmp = [[0,1,2],[0,2,1]]
    return tmp

def returnCurrenciesData(data,currency):
    for currencies in data["data"]:
        if currencies["currency"] == currency:
            return currencies

def returnCurrenciesDataFROMTO(data,ffrom,to):
    currencies = returnCurrenciesData(data,ffrom)
    for trades in currencies["trades"]:
        if trades["change_to"] == to:
            return trades

def algorithm(forex,start_currency,start_value):
    tmp = forex["gielda"].length
    combination = generateCombinationOfThree(tmp)

    for i in combination:
        valueon1 = start_value
        max_value = 0

        g1 = forex["gielda"][ i[0] ]
        g2 = forex["gielda"][ i[1] ]
        g3 = forex["gielda"][ i[2] ]
        #data for start_currency in g1
        currenciesg1 = returnCurrenciesData(g1,start_currency)
        
        for change_to_ong1 in currenciesg1["trades"]:
            currenciesg2 = returnCurrenciesData(g2,change_to_ong1["currency"])
            
            for change_to_ong2 in currenciesg2["trades"]:
                if change_to_ong2["currency"] == start_value:
                    continue
                change_to_ong3 = returnCurrenciesDataFROMTO(g3,change_to_ong2["currency"],start_currency)

                
