from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('test/<str:symbol>', views.show, name='show'),
]