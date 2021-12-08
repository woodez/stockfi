import yfinance as yf

class Info:
   
   def __init__(self, name):
       self.name = name
       self.data = yf.Ticker(name).info

   def get_longName(self):
       return(self.data.get('longName', "NA"))