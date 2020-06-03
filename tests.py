import unittest
import json 
from algo import *

class TestAlgo(unittest.TestCase):
    def testreturnSpecyficCurrencyFromData(self):
        data = {
            "nazwa":"gielda1",
            "currencies":["BTC","ETH","LTG"],
            "data":[
                {
                    "currency":"BTC",
                    "trades":[
                        {
                            "change_to":"ETH",
                            "records":[
                                {
                                    "date":1,
                                    "rate":1

                                },
                                {
                                    "date":2,
                                    "rate":1

                                }
                            ]
                        }
                    ]

                },
                {
                     "currency":"ETH",
                    "trades":[
                        {
                            "change_to":"LTG",
                            "records":[
                                {
                                    "date":1,
                                    "rate":1

                                },
                                {
                                    "date":2,
                                    "rate":1

                                }
                            ]
                        }
                    ]
                }
            ]
        }
        result = {
                    "currency":"ETH",
                    "trades":[
                        {
                            "change_to":"LTG",
                            "records":[
                                {
                                    "date":1,
                                    "rate":1

                                },
                                {
                                    "date":2,
                                    "rate":1

                                }
                            ]
                        }
                    ]
                }
        result2 ={
                    "currency":"BTC",
                    "trades":[
                        {
                            "change_to":"ETH",
                            "records":[
                                {
                                    "date":1,
                                    "rate":1

                                },
                                {
                                    "date":2,
                                    "rate":1

                                }
                            ]
                        }
                    ]

                } 
        self.assertEqual(result,returnSpecyficCurrencyFromData(data,"ETH"))
        self.assertEqual(result2,returnSpecyficCurrencyFromData(data,"BTC"))

    def testreturnSpecyficCurrenciesInTrades(self):
        data = {
            "nazwa":"poloniex",
            "currencies":["BTC","ETH","LTG"],
            "data":[
                {
                    "currency":"BTC",
                    "trades":[
                        {
                            "change_to":"ETH",
                            "records":[
                                {
                                    "date":1,
                                    "rate":1

                                },
                                {
                                    "date":2,
                                    "rate":1

                                }
                            ]
                        },{
                            "change_to":"LTG",
                            "records":[
                                {
                                    "date":1,
                                    "rate":1

                                },
                                {
                                    "date":2,
                                    "rate":1

                                }
                            ]
                        },{
                            "change_to":"ABC",
                            "records":[
                                {
                                    "date":1,
                                    "rate":1

                                },
                                {
                                    "date":2,
                                    "rate":1

                                }
                            ]
                        }

                    ]

                },
                {
                     "currency":"ETH",
                    "trades":[
                        {
                            "change_to":"LTG",
                            "records":[
                                {
                                    "date":1,
                                    "rate":1

                                },
                                {
                                    "date":2,
                                    "rate":1

                                }
                            ]
                        }
                    ]
                }
            ]
        }
        
        result = {
                            "change_to":"LTG",
                            "records":[
                                {
                                    "date":1,
                                    "rate":1

                                },
                                {
                                    "date":2,
                                    "rate":1

                                }
                            ]
                        }
        self.assertEqual(result,returnSpecyficCurrenciesInTrades(data,"BTC","LTG"))

    def testreturnSpecyficRecord(self):
        data = {
                            "change_to":"LTG",
                            "records":[
                                {
                                    "date":1,
                                    "rate":1

                                },
                                {
                                    "date":2,
                                    "rate":1
                                },
                                {
                                    "date":3,
                                    "rate":5
                                },
                                {
                                    "date":4,
                                    "rate":1
                                }
                            ]
                        }
        record = 2
        result = 5
        self.assertEqual(result,returnSpecyficRecord(data,record))

    def testalgorithm(self):
        data = {
            "gielda":[{
            "nazwa":"gielda1",
            "currencies":["BTC","ETH","LTG"],
            "data":[
                {
                    "currency":"BTC",
                    "trades":[
                        {
                            "change_to":"ETH",
                            "records":[
                                {
                                    "date":1,
                                    "rate":138.23611

                                },
                                {
                                    "date":2,
                                    "rate":1

                                }
                            ]
                        },{
                            "change_to":"LTG",
                            "records":[
                                {
                                    "date":1,
                                    "rate":1

                                },
                                {
                                    "date":2,
                                    "rate":1

                                }
                            ]
                        }

                    ]

                },
                {
                     "currency":"ETH",
                    "trades":[
                        {
                            "change_to":"LTG",
                            "records":[
                                {
                                    "date":1,
                                    "rate":1

                                },
                                {
                                    "date":2,
                                    "rate":1

                                }
                            ]
                        },
                        {
                            "change_to":"BTC",
                            "records":[
                                {
                                    "date":1,
                                    "rate":1

                                },
                                {
                                    "date":2,
                                    "rate":1

                                }
                            ]
                        }
                    ]
                },
                {
                     "currency":"LTG",
                    "trades":[
                        {
                            "change_to":"ETH",
                            "records":[
                                {
                                    "date":1,
                                    "rate":1

                                },
                                {
                                    "date":2,
                                    "rate":1

                                }
                            ]
                        },
                        {
                            "change_to":"BTC",
                            "records":[
                                {
                                    "date":1,
                                    "rate":1

                                },
                                {
                                    "date":2,
                                    "rate":1

                                }
                            ]
                        }
                    ]
                }
            ]
        },
        {
            "nazwa":"gielda2",
            "currencies":["BTC","ETH","LTG"],
            "data":[
                {
                    "currency":"BTC",
                    "trades":[
                        {
                            "change_to":"ETH",
                            "records":[
                                {
                                    "date":1,
                                    "rate":1

                                },
                                {
                                    "date":2,
                                    "rate":1

                                }
                            ]
                        },{
                            "change_to":"LTG",
                            "records":[
                                {
                                    "date":1,
                                    "rate":1

                                },
                                {
                                    "date":2,
                                    "rate":1

                                }
                            ]
                        }

                    ]

                },
                {
                     "currency":"ETH",
                    "trades":[
                        {
                            "change_to":"LTG",
                            "records":[
                                {
                                    "date":1,
                                    "rate":2.52871

                                },
                                {
                                    "date":2,
                                    "rate":1

                                }
                            ]
                        },
                        {
                            "change_to":"BTC",
                            "records":[
                                {
                                    "date":1,
                                    "rate":1

                                },
                                {
                                    "date":2,
                                    "rate":1

                                }
                            ]
                        }
                    ]
                },
                {
                     "currency":"LTG",
                    "trades":[
                        {
                            "change_to":"ETH",
                            "records":[
                                {
                                    "date":1,
                                    "rate":1

                                },
                                {
                                    "date":2,
                                    "rate":1

                                }
                            ]
                        },
                        {
                            "change_to":"BTC",
                            "records":[
                                {
                                    "date":1,
                                    "rate":0.01894

                                },
                                {
                                    "date":2,
                                    "rate":1

                                }
                            ]
                        }
                    ]
                }
            ]
        },
        {
            "nazwa":"gielda3",
            "currencies":["BTC","ETH","LTG"],
            "data":[
                {
                    "currency":"BTC",
                    "trades":[
                        {
                            "change_to":"ETH",
                            "records":[
                                {
                                    "date":1,
                                    "rate":1

                                },
                                {
                                    "date":2,
                                    "rate":1

                                }
                            ]
                        },{
                            "change_to":"LTG",
                            "records":[
                                {
                                    "date":1,
                                    "rate":1

                                },
                                {
                                    "date":2,
                                    "rate":1

                                }
                            ]
                        }

                    ]

                },
                {
                     "currency":"ETH",
                    "trades":[
                        {
                            "change_to":"LTG",
                            "records":[
                                {
                                    "date":1,
                                    "rate":2.52871

                                },
                                {
                                    "date":2,
                                    "rate":1

                                }
                            ]
                        },
                        {
                            "change_to":"BTC",
                            "records":[
                                {
                                    "date":1,
                                    "rate":1

                                },
                                {
                                    "date":2,
                                    "rate":1

                                }
                            ]
                        }
                    ]
                },
                {
                     "currency":"LTG",
                    "trades":[
                        {
                            "change_to":"ETH",
                            "records":[
                                {
                                    "date":1,
                                    "rate":1

                                },
                                {
                                    "date":2,
                                    "rate":1

                                }
                            ]
                        },
                        {
                            "change_to":"BTC",
                            "records":[
                                {
                                    "date":1,
                                    "rate":0.01894

                                },
                                {
                                    "date":2,
                                    "rate":1

                                }
                            ]
                        }
                    ]
                }
            ]
        }
        
        
        
        ]}

        result = 1.03539
        fromalgo,order,date = algorithm(data,"BTC",1,2)
        fromalgo = round(fromalgo,5)
        self.assertEqual(result,fromalgo)
        print(order)
        print(generateCombinationOfThree(3))
        print(date)


if __name__ == '__main__':
    
    unittest.main()