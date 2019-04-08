from django.db import models

# Models for migrations

class Currency(models.Model):
    currency_from = models.CharField(max_length=3)
    currency_to = models.CharField(max_length=3)

class Exchange(models.Model):
    exchange_date = models.DateField()
    currency_id = models.ForeignKey(Currency, on_delete=models.CASCADE)
    exchange_rate = models.FloatField()
