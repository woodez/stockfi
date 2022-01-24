import yfinance as yf
import math
import pyarrow as pa
import redis
import sys
import warnings
warnings.filterwarnings("ignore")
import pandas as pd
from .graph import graph_btc_daily

# BTC-CAD-HIST -> historic
# BTC-CAD -> 1 day 1min interval

class Crypto:
   
   def __init__(self, mysatoshi):
       self.mysatoshi = mysatoshi

   def get_cached_df(self, datasource):
       pool = redis.ConnectionPool(host='redis01.woodez.net',port='6379', db=0) 
       cur = redis.Redis(connection_pool=pool)
       context = pa.default_serialization_context()
       all_keys = [key.decode("utf-8") for key in cur.keys()]

  #     if self.portfolio in all_keys:   
       result = cur.get(datasource)
       dataframe = pd.DataFrame.from_dict(context.deserialize(result))

       return dataframe

  #     return None
    
   def get_mybtc_table(self):
       crypto_data = self.get_cached_df("BTC-CAD-HIST")
#       crypto_data["myvalue"] = crypto_data['Close'] * self.mysatoshi
       my_btc = crypto_data['Close'] * self.mysatoshi
#       crypto_data['myvalue'] = crypto_data['myvalue'].pct_change() * 100
       pct_chg = '{:,.2f}'.format(my_btc.pct_change() * 100)
       crypto_data['myvalue'] = '{:,.2f}%({:,.2f})'.format(pct_chg,my_btc)
       crypto_data = crypto_data.tail(10)
       crypto_dict = crypto_data.to_dict()
       btc_dict = {}
       for line in sorted(crypto_dict.get('myvalue').keys(), reverse=True):
           key = str(line).split(" ")[0]
#           value = '${:,.2f}'.format(portfolio_dict.get('value')[line])
##           value = '{:,.2f}'.format(crypto_dict.get('myvalue')[line])
           value = crypto_dict.get('myvalue')[line]
           tmpdict = { key:value }
           btc_dict.update(tmpdict)
       return btc_dict

   def get_pct_change(self):
       crypto_data = self.get_cached_df("BTC-CAD")
       crypto_data["myvalue"] = crypto_data['Close'] * self.mysatoshi
       crypto_data = crypto_data.dropna()
       test = 100*(crypto_data["myvalue"].iloc[-1]/crypto_data["myvalue"].iloc[0]-1) 
       return '{:,.2f}'.format(test)

   def get_daily_price(self):
       crypto_data = self.get_cached_df("BTC-CAD")
       crypto_data = crypto_data.dropna()
       return graph_btc_daily(crypto_data)
  

# crypto_obj = Crypto(0.01677643)
# print(crypto_obj.get_pct_change())
# print(crypto_obj.get_mybtc_table())