from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from .forms import StockForm
from .graph import return_graph
from .info import Info

# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def show(request,symbol):
    info = Info(symbol)
    context = {
        'longName': info.get_longName(),
        'logo_url': info.get_logo_url(),        
        'avg': return_graph(symbol, 3, 'avg'),
        'volatility': return_graph(symbol, 3, 'volatility'),
        'symbol': symbol
    }
    return render(request, 'mybag/dashboard.html', context)

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
