from datetime import datetime

from django.db import models

# Create your models here.
class User(models.Model):
    # ID = models.IntegerField(max_length=10)
    Name = models.CharField(max_length=255)
    Address = models.CharField(max_length=255)
    CardNumber = models.CharField(max_length=255)
    CardPayment = models.BooleanField
class Product(models.Model):
    # ID = models.IntegerField(max_length=10)
    Name = models.CharField(max_length=255)
    Kind = models.CharField(max_length=255)
    Color = models.CharField(max_length=255,default="blue")
    Price = models.IntegerField(default=0)
    Size = models.CharField(max_length=20,default=0)

class Order(models.Model):
    Uid = models.BigIntegerField(default=0)
    Pid = models.BigIntegerField(default=0)
    time = models.DateTimeField(default=datetime.now())




