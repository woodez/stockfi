import yfinance as yf
import math
import pyarrow as pa
import redis
import sys
import warnings

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
       total = df['value'].values[0]
       return '${:,.2f}'.format(total)           
           