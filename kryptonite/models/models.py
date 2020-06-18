from django.contrib.auth.models import User
from django.db import models


class Currency(models.Model):
    label = models.CharField(max_length=30)
    value = models.CharField(max_length=30)


class Exchange(models.Model):
    label = models.CharField(max_length=30)
    value = models.CharField(max_length=30)
    transaction_fee = models.FloatField(default=0.02)


class FavouriteCurrency(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)


class FavouriteExchange(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE)


class TestScheduleLog(models.Model):
    time = models.CharField(max_length=50)
    message = models.CharField(max_length=100)


class HistoricalResults(models.Model):
    time = models.DateTimeField(unique_for_date=True)
    results = models.CharField(max_length=800)