from django.urls import path
from . import views

urlpatterns = [
 #   path('', views.index, name='index'),
    path('ai/<str:symbol>', views.show, name='show'),
    path('', views.stocklookup, name='stocklookup'),
]