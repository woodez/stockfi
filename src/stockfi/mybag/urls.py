from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ai/<str:symbol>', views.show, name='show'),
    path('bag/<str:portfolio_owner>', views.portfolio, name='portfolio'),
    path('crypto/', views.crypto, name='crypto'),
    path('mover/', views.mover, name='mover'),
    path('find/', views.stocklookup, name='stocklookup'),
]