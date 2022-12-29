import yfinance as yf
import math
import pyarrow as pa
import redis
import sys
import json
import time
import datetime
import warnings
import requests
warnings.filterwarnings("ignore")
import pandas as pd
# from .graph import graph_btc_daily

# BTC-CAD-HIST -> historic
# BTC-CAD -> 1 day 1min interval

class Crypto:
   
   def __init__(self, mysatoshi, mygwei):
       self.mysatoshi = mysatoshi
       self.mygwei = mygwei

   def get_cached_df(self, datasource):
####       url = "http://127.0.0.1:8000/api/{}".format(datasource)
####       response = requests.get(url)
####       df_json = response.json()
####       df_dict = json.loads(df_json)
####       column = df_dict.keys()
####       dataframe = pd.DataFrame(df_dict, columns = column)
#       print(type(dataframe))
       pool = redis.ConnectionPool(host='redis01.woodez.net',port='6379', db=0) 
       cur = redis.Redis(connection_pool=pool)
       context = pa.default_serialization_context()
       all_keys = [key.decode("utf-8") for key in cur.keys()]

  #     if self.portfolio in all_keys:   
       result = cur.get(datasource)
       dataframe = pd.DataFrame.from_dict(context.deserialize(result))

       return dataframe

  #     return None
    
   def get_mybtc_table(self,output,datatype,crypto):
       crypto_data = self.get_cached_df(datatype)
       print(crypto_data)
       if "satoshi" in crypto:
          crypto_data["myvalue"] = crypto_data['Close'] * self.mysatoshi
       else:
          crypto_data["myvalue"] = crypto_data['Close'] * self.mygwei
       if "pct" in output:
          crypto_data['myvalue'] = crypto_data['myvalue'].pct_change() * 100
       crypto_data = crypto_data.tail(10)
       crypto_dict = crypto_data.to_dict()
       btc_dict = {}
       for line in sorted(crypto_dict.get('myvalue').keys(), reverse=True):
           key = str(line).split(" ")[0]
           value = '{:,.2f}'.format(crypto_dict.get('myvalue')[line])
           tmpdict = { key:value }
           btc_dict.update(tmpdict)
       return btc_dict

   def get_pct_change(self,datasource):
       crypto_data = self.get_cached_df(datasource)
       if "BTC" in datasource:
           crypto_data["myvalue"] = crypto_data['Close'] * self.mysatoshi
       else:
           crypto_data["myvalue"] = crypto_data['Close'] * self.mygwei
       crypto_data = crypto_data.dropna()
       test = 100*(crypto_data["myvalue"].iloc[-1]/crypto_data["myvalue"].iloc[0]-1) 
       return '{:,.2f}'.format(test)

   def get_std_value(self,datasource): 
       crypto_data = self.get_cached_df(datasource)
       test = crypto_data["Close"].std(axis= 0, skipna = True)
       return '{:,.2f}'.format(test)


   def get_current_price(self,datasource):
       crypto_data = self.get_cached_df(datasource)
       price = crypto_data['Close'].tail(1)[0]
       return '{:,.2f}'.format(price)

   def get_daily_price(self,datasource):
       crypto_data = self.get_cached_df(datasource)
       crypto_data = crypto_data.dropna()
       return graph_btc_daily(crypto_data,"daily")

   def get_hist_btc(self,datasource):
       crypto_data = self.get_cached_df(datasource)
       crypto_data = crypto_data.dropna()
       return graph_btc_daily(crypto_data,"hist") 

#  SQ-trend
   ##def get_stock_trend(self):
     ##  symbol = "{}-trend".format("SQ")
     ##  stock_data = self.get_cached_df(symbol)
     ##  # return stock_data
     ##  return graph_btc_daily(stock_data)
     ##  #return graph_stock_daily(stock_data,symbol)
crypto_obj = Crypto(0.01677643,0.09893748)
df = crypto_obj.get_current_price("BTC-CAD")

# crypto_obj = Crypto(0.01677643,0.007978979)
##df = crypto_obj.get_cached_df("BTC-CAD")
#print(df)
##df_json = df.to_json()
##df_dict = json.loads(df_json)
##column = df_dict.keys()
##df1 = pd.DataFrame(df_dict, columns = column)
##print(df1)

##print(type(df1))
# print(crypto_obj.get_stock_trend("SQ"))
# print(crypto_obj.get_current_price())
print(crypto_obj.get_mybtc_table("normal","BTC-CAD-HIST","satoshi"))