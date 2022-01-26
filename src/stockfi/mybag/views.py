from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from .forms import StockForm
from .graph import return_graph
from .graph import pie_portfolio_holdings
from .graph import pie_portfolio_value
from .graph import portfolio_percent_holdings
from .info import Info
from .portfolio import Portfolio
from .crypto import Crypto
from .models import MyBag

# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def show(request,symbol):
    data = return_graph(symbol, 3, 'avg')
    graph = data.get('graph', "NA")
    current_ma200 = data.get('current_ma200', "NA")
    info = Info(symbol, current_ma200)
    context = {
        'longName': info.get_longName(),
        'logo_url': info.get_logo_url()
        'long_sum': info.get_longBusinessSummary(),
        'stock_rating': info.get_stock_rating(),
        'avg': graph,
        'volatility': return_graph(symbol, 3, 'volatility'),
        'recommendationMean': info.get_mean(),
        'priceToBook': info.get_pb(),
        'debtToEquity': info.get_debttoequity(),
        'marketCap': info.get_marketCap(),
        'volume': info.get_volume(),
        'averageVolume10day': info.get_averageVolume10day(),
        'MarketPrice': info.regularMarketPrice(),
        'averageVolume': info.get_averageVolume(),
        'fiftyDayAverage': info.get_fiftyDayAverage(),
        'twoHundredDayAverage': info.get_twoHundredDayAverage(),
        'previousClose': info.get_previousClose(),
        'returnOnEquity': info.get_returnOnEquity(),
        'open': info.get_open(),
        'symbol': symbol
    }
    return render(request, 'mybag/test.html', context)

def stocklookup(request):

    if request.method == 'POST':
        form = StockForm(request.POST)

        if form.is_valid():
            stock_symbol = form.cleaned_data['stock_symbol']
            stock_symbol_upper = stock_symbol.upper()
            return HttpResponseRedirect(f'/stock/ai/{stock_symbol_upper}', {'stock_symbol':stock_symbol_upper})

    else:
        form = StockForm()
        context ={
            'form':form,
        }
    return render(request, 'mybag/create.html', context)

def portfolio(request,portfolio_owner):
    portfolio_list = MyBag.objects.all()
    stock_list = []
    stock_dict = {}
    for i, obj in enumerate(portfolio_list):
        if obj.username == portfolio_owner and obj.number_shares != 0:
           stock_list.append(obj.stock_ticker)
           tmpdict = { obj.stock_ticker: obj.number_shares}
           stock_dict.update(tmpdict)
        else:
           stock_list = ["empty"]
           context = {
               'stock_list': stock_list
           }
    portfolio_obj = Portfolio("woodez")
    port_value = portfolio_obj.get_porfolio_value()
    port_trend = portfolio_obj.get_daily_trend()
    port_graph = portfolio_obj.get_portfolio_graph()
    holding_pie = pie_portfolio_holdings(stock_dict)
    cap_pie = pie_portfolio_value()
    port_dict = portfolio_obj.get_portfolio_table()
    port_std = portfolio_obj.get_portfolio_std()
    port_pct_chg = portfolio_obj.get_pct_change
    sorted_dict = {}
    sorted_keys = sorted(stock_dict, key=stock_dict.get, reverse=True)
    for w in sorted_keys:
        sorted_dict[w] = stock_dict[w]
    context = {
       'stock_dict': sorted_dict,
       'portfolio_total': port_value,
       'portfolio_trend': port_trend,
       'portfolio_graph': port_graph,
       'portfolio_holdings': holding_pie,
       'portfolio_cap': cap_pie,
       'portfolio_data': port_dict,
       'port_std': port_std,
       'percent_change': port_pct_chg,
       'portfolio_pct_tbl': portfolio_percent_holdings()
    }
    return render(request, 'mybag/portfolio.html', context)

def crypto(request):
    crypto_obj = Crypto(0.01677643)
    my_btc_table_pct = crypto_obj.get_mybtc_table("pct")
    my_btc_table = crypto_obj.get_mybtc_table("normal")
    btc_current = crypto_obj.get_current_price()
    btc_day_trend = crypto_obj.get_pct_change()
    btc_daily_graph = crypto_obj.get_daily_price()
    btc_hist_graph = crypto_obj.get_hist_btc()

    context = {
        'crypto_port': my_btc_table,
        'btc_day_trend': btc_day_trend,
        'btc_current': btc_current,
        'btc_daily_graph': btc_daily_graph,
        'btc_hist_graph': btc_hist_graph
    }
    return render(request, 'mybag/cypto.html', context)