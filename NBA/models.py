from django.db import models

# Create your models here.
class Schedule(models.Model):
    team = models.CharField(max_length=30)
    date = models.CharField(max_length=10)
    opponent = models.CharField(max_length=30)
    time = models.CharField(max_length=10)
    channel = models.CharField(max_length=100)