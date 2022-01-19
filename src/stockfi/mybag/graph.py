import pandas as pd
from io import StringIO
from datetime import date
import numpy as np
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix
import yfinance as yf
import pyarrow as pa
import redis
import warnings
warnings.filterwarnings("ignore")

def get_cached_df(alias):
    pool = redis.ConnectionPool(host='redis01.woodez.net',port='6379', db=0) 
    cur = redis.Redis(connection_pool=pool)
    context = pa.default_serialization_context()
    all_keys = [key.decode("utf-8") for key in cur.keys()]

    if alias in all_keys:   
        result = cur.get(alias)

        dataframe = pd.DataFrame.from_dict(context.deserialize(result))

        return dataframe

    return None


def return_graph(symbol,years,gtype):
    d = date.today()
    start = d.replace(year=d.year - years).strftime("%Y-%m-%d")
    end = d.strftime("%Y-%m-%d")
    btc = get_cached_df(symbol)
#    btc = yf.download(symbol,start,end)
    plt.clf()
    if "avg" in gtype:
       btc['MA50'] = btc['Open'].rolling(50).mean()
       btc['MA200'] = btc['Open'].rolling(200).mean()
       btc['Open'].plot(label = symbol, figsize = (15,7))
       btc['MA50'].plot(label = "MA50")
       btc['MA200'].plot(label = "MA200")
       plt.title("{}".format(symbol))
       plt.legend()
       imgdata = StringIO()
       plt.grid()
       plt.savefig(imgdata, format='svg')
       imgdata.seek(0)
       current_ma200_value = btc['MA200'].tail(1).values[0]
       data = imgdata.getvalue()
       plt.figure().clear()
       plt.close()
       plt.cla()
       plt.clf()
       return { "graph": data, "current_ma200": current_ma200_value }
    else: 
       btc['returns'] = (btc['Close']/btc['Close'].shift(1)) -1
       btc['returns'].hist(bins = 100, label = symbol, alpha = 0.5, figsize = (15,7))
       plt.title("Daily Volatility of {}".format(symbol))
       plt.legend()
       imgdata = StringIO()
       plt.savefig(imgdata, dpi=50, format='svg')
       imgdata.seek(0)
       data = imgdata.getvalue()
       plt.figure().clear()
       plt.close()
       plt.cla()
       plt.clf()
       return data

def graph_portfolio(portfolio_data, name):
    portfolio_data['value'].plot(label = "Woodez Innovation Fund", figsize = (7,5))
    plt.title("{}".format("Woodez Innovation Fund"))
    plt.legend()
    imgdata = StringIO()
    plt.grid()
    plt.savefig(imgdata, format='svg')
    imgdata.seek(0)
    data = imgdata.getvalue()
    plt.figure().clear()
    plt.close()
    plt.cla()
    plt.clf()
    return data

def pie_portfolio_holdings(stock_dict):
    tickers = []
    volume = []
    for line in stock_dict.keys():
        if stock_dict[line] != 0:
           tickers.append(line)
           volume.append(stock_dict[line])

    details = {
        'Name': tickers,
        'Amount': volume,
    }

    df = pd.DataFrame(details)
    fig = plt.figure(label = "Woodez Innovation Fund", figsize =(10, 7))
    plt.pie(df['Amount'], labels = df['Name'])
    plt.title("{}".format("Woodez Innovation Fund"))
    plt.legend()
    imgdata = StringIO()
    plt.savefig(imgdata, format='svg')
    data = imgdata.getvalue()
    plt.figure().clear()
    plt.close()
    plt.cla()
    plt.clf()
    return data
#    x = np.arange(0,np.pi*3,.1)
#    y = np.sin(x)
#    fig = plt.figure()
#    plt.plot(x,y)
#    imgdata = StringIO()
#    fig.savefig(imgdata, format='svg')
#    imgdata.seek(0)
#    data = imgdata.getvalue()
#    return data