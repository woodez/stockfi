import yfinance as yf
import math

# regularMarketPrice': 314.04,

class Portfolio:
   
   def __init__(self, stockdata):
       self.stockdata = stockdata

   def get_close_value(self, ticker):
       data = yf.Ticker(ticker).info
       return data['regularMarketPrice']

   def get_porfolio_value(self):
       value_list = []
       for key, value in self.stockdata.items():
           price = self.get_close_value(key)
           market_value = float(price) * float(value)
           value_list.append(market_value)
       total = math.fsum(value_list)
       return '${:,.2f}'.format(total)           
           