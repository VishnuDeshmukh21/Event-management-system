
from django.db import models

class Event(models.Model):
    event_name = models.CharField(max_length=100)
    city_name = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    latitude = models.DecimalField(max_digits=10, decimal_places=8)
    longitude = models.DecimalField(max_digits=11, decimal_places=8)

