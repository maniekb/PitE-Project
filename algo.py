import numpy as np
import json


class Alg:

    def generate_element(self,forexname,to,day,minute,price):
        element = {
            "to": to,
            "day": day,
            "minute": minute,
            "price":price
        }
        return element

    def addToCurrencies(self,curr,toadd):
        curr["currencies"].append(toadd)

    def addElementToCurrency(self,currencies,currency,elem):
        
        for tmp in currencies["currencies"]:
            if tmp == currency :
                tmp["elements"].append(elem)

    def generate_data(self):
        forex = {
            "currencies":[]
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