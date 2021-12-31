from django.db import models

class MyBag(models.Model):
    username = models.CharField(max_length=80)
    stock_ticker = models.CharField(max_length=20)
    number_shares = models.IntegerField()
