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

   def get_cached_df(self, portfolio_name):
       pool = redis.ConnectionPool(host='redis01.woodez.net',port='6379', db=0) 
       cur = redis.Redis(connection_pool=pool)
       context = pa.default_serialization_context()
       all_keys = [key.decode("utf-8") for key in cur.keys()]

       if self.portfolio in all_keys:   
           result = cur.get(portfolio_name)
           dataframe = pd.DataFrame.from_dict(context.deserialize(result))

           return dataframe

       return None

   def get_porfolio_value(self):
       df = self.get_cached_df(self.portfolio).tail(1)
       total = float(df['value'].values[0])
       return '${:,.2f}'.format(total) 

#   df_redis = get_cached_df("woodez_sentiment")
   def get_daily_sentiment(self):
       df = self.get_cached_df("woodez_sentiment").tail(1)
       total = float(df['value'].values[0])
       return '{:,.2f}'.format(total)


   def get_portfolio_std(self):
       # A low standard deviation indicates that the values tend to be close to the mean 
       # (also called the expected value) of the set, while a high standard 
       # deviation indicates that the values are spread out over a wider range
       df = self.get_cached_df(self.portfolio)
       df["value"] = pd.to_numeric(df["value"], downcast="float")
       return df["value"].std(axis= 0, skipna = True)

   def get_portfolio_mean(self):
       df = self.get_cached_df(self.portfolio)
       df["value"] = pd.to_numeric(df["value"], downcast="float")
       return df["value"].mean(axis= 0, skipna = True)

#   df_redis = get_cached_df("woodez_sentiment")

   def get_pct_change(self):
       df = self.get_cached_df(self.portfolio)
       df["value"] = pd.to_numeric(df["value"], downcast="float")
       test = 100*(df["value"].iloc[-1]/df["value"].iloc[0]-1) 
#       df["pct_change"] = df["value"].pct_change()
#       index = df["pct_change"].size - 1
#       return '{:,.2f}'.format(df["pct_change"][index] * 100)
       return '{:,.2f}'.format(test)

   def get_portfolio_graph(self):
       portfolio_data = self.get_cached_df(self.portfolio)
       portfolio_data["value"] = pd.to_numeric(portfolio_data["value"], downcast="float")
       portfolio_data["Date"] = pd.to_datetime(portfolio_data["date"])
       portfolio_data = portfolio_data.set_index('Date')
       return graph_portfolio(portfolio_data, self.portfolio)

   def get_portfolio_table(self):
       portfolio_data = self.get_cached_df(self.portfolio)
       portfolio_data["value"] = pd.to_numeric(portfolio_data["value"], downcast="float")
       portfolio_data["Date"] = pd.to_datetime(portfolio_data["date"])
       portfolio_data["value"] = portfolio_data["value"].pct_change() * 100
       portfolio_data = portfolio_data.tail(10)
       portfolio_data = portfolio_data.set_index('Date')
       portfolio_dict = portfolio_data.to_dict()
       port_dict = {}
       for line in sorted(portfolio_dict.get('value').keys(), reverse=True):
           key = str(line).split(" ")[0]
#           value = '${:,.2f}'.format(portfolio_dict.get('value')[line])
           value = '{:,.2f}'.format(portfolio_dict.get('value')[line])
           tmpdict = { key:value }
           port_dict.update(tmpdict)
       return port_dict
   
   def get_daily_trend(self):
       df = self.get_cached_df(self.portfolio).tail(2)
       latest = float(df['value'].values[1])
       nextup = float(df['value'].values[0])
       if latest < nextup:
           portfolio_trend = "Todays Trend is Down"
       else:
           portfolio_trend = "Todays Trend is Up"

       return portfolio_trend



# portfolio_obj = Portfolio("woodez")
# port_std = portfolio_obj.get_daily_sentiment()
# print(port_std)
# port_std = portfolio_obj.get_portfolio_std()
# port_mean = portfolio_obj.get_portfolio_mean()
# pct_chg = portfolio_obj.get_pct_change()
# print(port_std)
# print(port_mean)
# print(pct_chg)
           