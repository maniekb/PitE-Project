# Kryptonite
## Participants 
 - **Maciej Bolsęga**
 - Piotr Brunarski
 - Maciej Dworak
 - Piotr Ksel

## Demo
Demo of application (in early development phase) available here: https://kryptonite-pite.herokuapp.com/ <br>
If run locally, first need to use these commands in project directory: <br>
`pip install -r requirements.txt` <br>
`python manage.py collectstatic` <br>
`python manage.py runserver` <br>

## Introduction
Idea of the project is to create application which gather data from external APIs about current cryptocurrency rates. It will create charts representing these rates. Further it will be able to calculate possible arbitrage trades - making profit out of buying/selling crypto based on price differences between markets (including margin).

More information about arbitrage algorithm available in `doc/algorithm_description.md`

## Technology
We’ll use template system of Django framework to generate simple UI. As long as APIs provide historical data we won’t store any data in database - unless we find out during implementation it’s necessary.

## APIs  
https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md <br> 
https://docs.poloniex.com/#introduction <br>
https://docs.bitfinex.com/docs/introduction <br>
https://bittrex.github.io/api/v3 <br>

## Week Plan
**Week 1**
- 1.1 In-depth research of APIs 
- 1.3 Create UI concept
- 1.2 Setting empty project
- 1.3 Connect and gather some data from any API
- 1.4 Testing

**Week 2**
- 2.1 Preparing own model of data for further processing
- 2.2 Adapting data from one API to our data model
- 2.3 Creating web-page based on UI design
- 2.4 Design of arbitrage algorithm
- 2.4 Testing

**Week 3**
- 3.1 Show data on the web page (preferably any type of chart)
- 3.2 Adapting data of other APIs to our data model
- 3.3 First implementation of arbitrage algorithm
- 3.4 Testing

**Week 4**
- 4.1 Further development of algorithm (including margin)
- 4.2 Displaying effects of algorithm on web-page
- 4.3 Expanding range of markets and currencies
- 4.4 Testing

**Week 5**
- 5.1 Working on efficiency and correctness of arbitrage algorithm
- 5.2 Improving UI and displaying all functionalities
- 5.3 Testing

**Week 6**
- 6.1 Quality assurance
- 6.2 Final adjustments
