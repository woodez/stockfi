import pandas as pd
import datetime
import numpy as np
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix
import yfinance as yf
# %matplotlib inline

start = "2021-01-01"
end = '2021-11-14'
btc = yf.download('BTC-CAD',start,end)
eth = yf.download('ETH-CAD',start,end)

btc['Open'].plot(label = 'BTC', figsize = (15,7))
eth['Open'].plot(label = "ETH")
plt.title('BTC, ETH')
plt.show()