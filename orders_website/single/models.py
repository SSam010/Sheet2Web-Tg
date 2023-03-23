from django.db import models


class Orders(models.Model):
    id = models.IntegerField(unique=True, primary_key=True)
    order_number = models.IntegerField(unique=True)
    price_usd = models.IntegerField()
    delivery_time = models.DateField()
    price_rub = models.IntegerField()


