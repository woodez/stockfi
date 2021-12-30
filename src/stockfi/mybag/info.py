import yfinance as yf

class Info:
   
   def __init__(self, name, current_ma200):
       self.name = name
       self.current_ma200 = current_ma200
       self.data = yf.Ticker(name).info

   def get_longName(self):
       return(self.data.get('longName', "NA"))

   def get_logo_url(self):
       return(self.data.get('logo_url', "NA"))

   def get_longBusinessSummary(self):
       return(self.data.get('website', "NA")) 

   def get_mean(self):
       return(self.data.get('recommendationMean', "NA"))

   def get_pb(self):
       return(self.data.get('priceToBook', "NA"))

   def get_debttoequity(self):
       return(self.data.get('debtToEquity', "NA"))

   def get_marketCap(self):
       return(self.data.get('marketCap', "NA"))
    
   def get_volume(self):
       return(self.data.get('volume', "NA"))

   def get_averageVolume10day(self):
       return(self.data.get('averageVolume10day', "NA"))
    
   def get_averageVolume(self):
       return(self.data.get('averageVolume', "NA"))

   def get_fiftyDayAverage(self):
       return(self.data.get('fiftyDayAverage', "NA"))

   def get_twoHundredDayAverage(self):
       return(self.data.get('twoHundredDayAverage', "NA"))

   def get_previousClose(self):
       return(self.data.get('previousClose', "NA"))

   def get_open(self):
       return(self.data.get('open', "NA"))
    
   def get_returnOnEquity(self):
       percent = "{:.0%}".format(float(self.data.get('returnOnEquity', "NA")))
       return(percent)
   
   def get_stock_rating(self):
       current_open = self.data.get('open', "9000")
       if int(current_open) < int(self.current_ma200):
          rating = 'Woodez Buy Rating'
       else:
          rating = "Woodez HODL Rating"
       return(rating)