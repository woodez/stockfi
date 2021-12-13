from django import forms

class StockForm(forms.Form):
    stock_symbol = forms.CharField(label = "Stock Search",max_length =240)