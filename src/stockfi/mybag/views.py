from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from .forms import StockForm
from .graph import return_graph
from .info import Info
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
        'logo_url': info.get_logo_url(),
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
    sorted_dict = {}
    sorted_keys = sorted(stock_dict, key=stock_dict.get)
    for w in sorted_keys:
        sorted_dict[w] = stock_dict[w]
    context = {
       'stock_dict': sorted_dict,
    }
    return render(request, 'mybag/portfolio.html', context)



