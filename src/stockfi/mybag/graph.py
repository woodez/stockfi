import pandas as pd
from io import StringIO
import datetime
import numpy as np
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix
import yfinance as yf

def return_graph():
    start = "2021-01-01"
    end = '2021-11-28'
    btc = yf.download('BTC-CAD',start,end)

    btc['Open'].plot(label = 'BTC', figsize = (15,7))
    plt.title('BTC open price')
    imgdata = StringIO()
    plt.savefig(imgdata, format='svg')
    imgdata.seek(0)
    data = imgdata.getvalue()
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