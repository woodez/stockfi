import pandas as pd
from io import StringIO
from datetime import date
import numpy as np
import matplotlib
# matplotlib.use('agg')
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix
import io, base64
import yfinance as yf
import pyarrow as pa
import redis
import sys
import warnings
warnings.filterwarnings("ignore")

#get_cached_df("woodez_portfolio_details")

def get_cached_df(alias):
    pool = redis.ConnectionPool(host='redis01.woodez.net',port='6379', db=0) 
    cur = redis.Redis(connection_pool=pool)
    context = pa.default_serialization_context()
    all_keys = [key.decode("utf-8") for key in cur.keys()]

#    if alias in all_keys:   
    result = cur.get(alias)
    dataframe = pd.DataFrame.from_dict(context.deserialize(result))

    return dataframe


def return_graph(symbol,years,gtype):
    d = date.today()
    start = d.replace(year=d.year - years).strftime("%Y-%m-%d")
    end = d.strftime("%Y-%m-%d")
    ticker = "{}-trend".format(symbol)
    stockday = get_cached_df(ticker)
##    symbol = "{}-trend".format(symbol)
    btc = get_cached_df(symbol)
#    btc = yf.download(symbol,start,end)
    if "avg" in gtype:
       plt.close()
       btc['MA5'] = btc['Close'].rolling(5).mean()
       btc['MA50'] = btc['Close'].rolling(50).mean()
       btc['MA200'] = btc['Close'].rolling(200).mean()
       btc['Open'].plot(label = symbol, figsize = (15,7))
       btc['MA5'].plot(label = "MA5")
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
#       plt.figure().clear()
#       plt.close()
#       plt.cla()
#       plt.clf()
       return { "graph": data, "current_ma200": current_ma200_value }
    elif "volatility" in gtype:
       plt.close()
       btc['returns'] = (btc['Close']/btc['Close'].shift(1)) -1
       btc['returns'].hist(bins = 100, label = symbol, alpha = 0.5, figsize = (15,7))
       plt.title("Daily Volatility of {}".format(symbol))
       plt.legend()
       imgdata = StringIO()
       plt.savefig(imgdata, dpi=50, format='svg')
       imgdata.seek(0)
       data = imgdata.getvalue()
    #   plt.figure().clear()
    #   plt.close()
    #   plt.cla()
    #   plt.clf()
       return data 
    else:
       plt.close()
       stockday = get_cached_df(ticker)
       stockday['Close'].plot(label = symbol, figsize = (15,7))
       plt.title("Daily Movement of {}".format(symbol))
       plt.legend()
       imgdata = StringIO()
       plt.savefig(imgdata, dpi=50, format='svg')
       imgdata.seek(0)
       data = imgdata.getvalue()
    #   plt.figure().clear()
    #   plt.close()
    #   plt.cla()
    #   plt.clf()
       return data 


def graph_portfolio(portfolio_data, name):
    plt.close()
    portfolio_data["value"] = pd.to_numeric(portfolio_data["value"], downcast="float")
    portfolio_data['pct_change'] = portfolio_data['value'].pct_change() * 100 
    portfolio_data['pct_change'].plot(figsize = (7,5))
    plt.title("{}".format("Woodez Innovation Fund"))
    imgdata = StringIO()
    plt.grid()
    plt.savefig(imgdata, format='svg')
    imgdata.seek(0)
    data = imgdata.getvalue()
    # plt.figure().clear()
    # plt.close()
    # plt.cla()
    # plt.clf()
    return data


def graph_portfolio_sentiment():
    portfolio_sent = get_cached_df("woodez_sentiment")
    print(portfolio_sent)
    plt.close()
    portfolio_sent["value"] = pd.to_numeric(portfolio_sent["value"], downcast="float")
    portfolio_sent["value"].plot(figsize = (7,5))
    plt.title("{}".format(Woodez Innovation Fund Sentiment))
    imgdata = StringIO()
    plt.grid()
    plt.savefig(imgdata, format='svg')
    imgdata.seek(0)
    data = imgdata.getvalue()
    return data

def graph_btc_daily(crypto_data,type):
    if "daily" in type:
       plt.close() 
       crypto_data['STD'] = crypto_data['Close'].rolling(60).std()
       crypto_data['Close'].plot(label = "Daily BTC", figsize = (7,5))
       crypto_data['STD'].plot(label = "STD")
       plt.title("{}".format("Daily BTC"))
       plt.legend()
       plt.grid()
       imgdata = StringIO()
       plt.savefig(imgdata, format='svg')
       data = imgdata.getvalue()
    #   plt.figure().clear()
    #   plt.close()
    #   plt.cla()
    #   plt.clf()
       return data
    else: 
       plt.clf() 
       plt.close() 
#       crypto_data['MA5'] = crypto_data['Close'].rolling(5).mean()
#       crypto_data['MA50'] = crypto_data['Close'].rolling(50).mean()
       crypto_data['MA200'] = crypto_data['Close'].rolling(200).mean()
       crypto_data['STD'] = crypto_data['Close'].rolling(50).std()
       crypto_data['Close'].plot(label = "Close", figsize = (7,5))
#       crypto_data['MA5'].plot(label = "MA5")
#       crypto_data['MA50'].plot(label = "MA50")
       crypto_data['MA200'].plot(label = "MA200")
       crypto_data['STD'].plot(label = "STD")
       plt.title("{}".format("Historical BTC"))
       plt.legend()
       plt.grid()
       imgdata = StringIO()
       plt.savefig(imgdata, format='svg')
       data = imgdata.getvalue()
#       plt.figure().clear()
#       plt.close()
#       plt.cla()
#       plt.clf()
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
    fig = plt.figure(figsize =(7,5))
    plt.pie(df['Amount'], labels = df['Name'])
    plt.title("{}".format("Woodez Innovation Fund Holdings"))
    imgdata = StringIO()
    plt.savefig(imgdata, format='svg')
    data = imgdata.getvalue()
    plt.figure().clear()
    plt.close()
    plt.cla()
    plt.clf()
    return data

def pie_portfolio_value():
    df = get_cached_df("woodez_portfolio_details")
    fig = plt.figure(figsize =(7,5))
#    plt.pie(df['Amount'], labels = df['Name'], autopct='%.0f%%', wedgeprops={'linewidth': 2.0, 'edgecolor': 'white'}, textprops={'size': 'x-small'})
    plt.pie(df['Amount'], wedgeprops={'linewidth': 2.0, 'edgecolor': 'white'}, textprops={'size': 'x-small'})
    plt.title("{}".format("Innovation Fund Capital Distribution"))
    plt.legend(df['Name'])
    plt.tight_layout()
    imgdata = StringIO()
    plt.savefig(imgdata, format='svg')
    data = imgdata.getvalue()
    plt.figure().clear()
    plt.close()
    plt.cla()
    plt.clf()
    return data

def portfolio_percent_holdings():
    df = get_cached_df("woodez_portfolio_details")
    total = float(df['Amount'].sum())
    
    percentage = []
    for value in df['Amount']:
        pct = (value/total) * 100
        percentage.append(round(pct, 2))
    df['Percentage'] = percentage   
    
    hist = {}
    for index, row in df.iterrows():
        tmpdict = { row['Name']:row['Percentage'] }
        hist.update(tmpdict)
    sorted_dict = {}
    sorted_keys = sorted(hist, key=hist.get, reverse=True)
    for w in sorted_keys:
        sorted_dict[w] = hist[w]
    return sorted_dict

def stock_dict(hist,sorter,num,type):
    if "loosers" in type:
       test = dict((k, v) for k, v in hist.items() if float(v) < 0)
       if not test:
          hist = hist
          sorter = True
       else:  
          hist = test 
    if "gainers" in type:
       test = dict((k, v) for k, v in hist.items() if float(v) >= 0)
       if not test:
          sorter = True
          hist = dict((k, v) for k, v in hist.items() if float(v) < 0)
    gainers_dict = {}
#    gainers_keys = sorted(hist.items(), key=lambda x: x[1], reverse=sorter)
    gainers_keys = sorted(hist.items(), key=lambda x: float(x[1]), reverse=sorter)
    for w in gainers_keys:
        gainers_dict[w[0]] = hist[w[0]]
    return dict(list(gainers_dict.items())[:num])

def stock_movers(num):
    df = get_cached_df("woodez_portfolio_details")
    df_close = get_cached_df("ticker_close")
    close_hist = {}

    for index, row in df_close.iterrows():
        tmpdict = { row['Name']:row['Amount'] }
        close_hist.update(tmpdict)

    hist = {}
    for index, row in df.iterrows():
        if "." not in row['Name'] and "-" not in row['Name']:
           symbol = row['Name']
           prevclose = float(close_hist[symbol])
           ticker = "{}-trend".format(row['Name'])           
           print(ticker)
           day_trend = get_cached_df(ticker)
           last_trade_day = float(day_trend["Close"].iloc[-1])
           difference = float(last_trade_day - prevclose)
           day_pct_chg = '{:,.2f}'.format(float(100 * (difference/prevclose)))
#           day_pct_chg = '{:,.2f}'.format(float(100*(day_trend["Close"].iloc[-1]/prevclose)))
           tmpdict = { row['Name']:day_pct_chg }
           hist.update(tmpdict)
    gainers_dict = stock_dict(hist, True, num, "gainers")
    loosers_dict = stock_dict(hist, False, num, "loosers")
    return { 'gainers':gainers_dict, 'loosers':loosers_dict } 



# graph_portfolio_sentiment()
####tickers = yf.Ticker('SQ').info['open']
## print(tickers)
#####test = stock_movers(5)
#####print(test)
###day_trend = get_cached_df("SQ-trend")
###print(day_trend['Datetime'])
# return_graph("SQ",3,"stockday")

# graph_stock_daily("SQ")

##        pct = (float(value['Amount']) / total)) * 100
##        print(pct)
#        percentage.append(round(pct, 2))
#    df['Percentage'] = percentage
#    print(df.to_dict('Percentage'))

# portfolio_percent_holdings()
#    x = np.arange(0,np.pi*3,.1)
#    y = np.sin(x)
#    fig = plt.figure()
#    plt.plot(x,y)
#    imgdata = StringIO()
#    fig.savefig(imgdata, format='svg')
#    imgdata.seek(0)
#    data = imgdata.getvalue()
#    return data