from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .graph import return_graph

# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def show(request):
    context = {
        'stock_graph': return_graph()
    }
    return render(request, 'mybag/dashboard.html', context)