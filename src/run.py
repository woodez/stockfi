import pandas as pd
from datetime import date
import numpy as np
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix
import yfinance as yf
# %matplotlib inline

many_years = 3
d = date.today()
year_back = d.replace(year=d.year - many_years).strftime("%Y-%m-%d")
today_date = d.strftime("%Y-%m-%d")
print('{0} and {1}'.format(today_date, year_back))

start = year_back
end = today_date
btc = yf.download('SQ',start,end)
eth = yf.download('ETH-CAD',start,end)
btc['MA200'] = btc['Open'].rolling(200).mean()

testing = btc['MA200'].tail(1).values[0]

print(testing)

# btc['Open'].plot(label = 'BTC', figsize = (15,7))
# plt.title('BTC, ETH')
# plt.show()