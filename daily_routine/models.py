
from datetime import datetime
from django.db import models

# Create your models here.


class DailyRoutine(models.Model):
    TIME_PERIOD_CHOICES = [
        ('morning', 'Morning'),
        ('afternoon', 'Afternoon'),
        ('evening', 'Evening'),
    ]
    
    date = models.DateTimeField(auto_now_add=True)
    age = models.IntegerField()
    mortality = models.IntegerField()
    time_period = models.CharField(choices=TIME_PERIOD_CHOICES, default="morning", max_length=100)
    feeding = models.IntegerField()
    drinking = models.IntegerField()
    medication = models.CharField(max_length=100)
    comment = models.TextField(blank=True)

