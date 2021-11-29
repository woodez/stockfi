from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .graph import return_graph

# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def show(request,symbol):
    context = {
        'avg': return_graph(symbol, 3, 'avg'),
        'volatility': return_graph(symbol, 3, 'volatility')
    }
    return render(request, 'mybag/dashboard.html', context)