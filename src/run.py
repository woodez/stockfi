import pandas as pd
from datetime import date
import numpy as np
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix
import yfinance as yf
# %matplotlib inline

many_years = 1
d = date.today()
year_back = d.replace(year=d.year - many_years).strftime("%Y-%m-%d")
today_date = d.strftime("%Y-%m-%d")
print('{0} and {1}'.format(today_date, year_back))

start = year_back
end = today_date
btc = yf.download('BTC-CAD',start,end)
eth = yf.download('ETH-CAD',start,end)

print(btc)

btc['Open'].plot(label = 'BTC', figsize = (15,7))
eth['Open'].plot(label = "ETH")
plt.title('BTC, ETH')
plt.show()