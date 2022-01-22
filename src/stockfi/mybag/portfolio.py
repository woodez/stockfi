import yfinance as yf
import math
import pyarrow as pa
import redis
import sys
import warnings
warnings.filterwarnings("ignore")
import pandas as pd
from .graph import graph_portfolio

# regularMarketPrice': 314.04,


class Portfolio:
   
   def __init__(self, portfolio):
       self.portfolio = portfolio

   def get_cached_df(self):

       pool = redis.ConnectionPool(host='redis01.woodez.net',port='6379', db=0) 
       cur = redis.Redis(connection_pool=pool)
       context = pa.default_serialization_context()
       all_keys = [key.decode("utf-8") for key in cur.keys()]

       if self.portfolio in all_keys:   
           result = cur.get(self.portfolio)
           dataframe = pd.DataFrame.from_dict(context.deserialize(result))

           return dataframe

       return None

   def get_porfolio_value(self):
       df = self.get_cached_df().tail(1)
       total = float(df['value'].values[0])
       return '${:,.2f}'.format(total) 

   def get_portfolio_std(self):
       # A low standard deviation indicates that the values tend to be close to the mean 
       # (also called the expected value) of the set, while a high standard 
       # deviation indicates that the values are spread out over a wider range
       df = self.get_cached_df()
       df["value"] = pd.to_numeric(df["value"], downcast="float")
       return df["value"].std(axis= 0, skipna = True)

   def get_portfolio_graph(self):
       portfolio_data = self.get_cached_df()
       portfolio_data["value"] = pd.to_numeric(portfolio_data["value"], downcast="float")
       portfolio_data["Date"] = pd.to_datetime(portfolio_data["date"])
       portfolio_data = portfolio_data.set_index('Date')
       return graph_portfolio(portfolio_data, self.portfolio)

   def get_portfolio_table(self):
       portfolio_data = self.get_cached_df().tail(10)
       portfolio_data["value"] = pd.to_numeric(portfolio_data["value"], downcast="float")
       portfolio_data["Date"] = pd.to_datetime(portfolio_data["date"])
       portfolio_data = portfolio_data.set_index('Date')
       portfolio_dict = portfolio_data.to_dict()
       port_dict = {}
       for line in sorted(portfolio_dict.get('value').keys(), reverse=True):
           key = str(line).split(" ")[0]
           value = '${:,.2f}'.format(portfolio_dict.get('value')[line])
           tmpdict = { key:value }
           port_dict.update(tmpdict)
       return port_dict
   
   def get_daily_trend(self):
       df = self.get_cached_df().tail(2)
       latest = float(df['value'].values[1])
       nextup = float(df['value'].values[0])
       if latest < nextup:
           portfolio_trend = "Todays Trend is Down"
       else:
           portfolio_trend = "Todays Trend is Up"

       return portfolio_trend


## portfolio_obj = Portfolio("woodez")
## port_std = portfolio_obj.get_portfolio_std()
## print(port_std)
           