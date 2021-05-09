from django.db import models
from django.utils import timezone
now = timezone.now()


class WakanowScrape(models.Model):
    user_email = models.CharField(max_length=500)
    passenger = models.CharField(max_length=500)
    passenger_email = models.CharField(max_length=300)
    details = models.CharField(max_length=300)
    flight = models.CharField(max_length=300)
    Total_Bill = models.CharField(max_length=300)
    Amount_Paid = models.CharField(max_length=500)
    Bill = models.CharField(max_length=500, default=0)
    paid_date = models.DateField()


class BeforePaymentData(models.Model):
    email = models.EmailField(max_length=100)
    web = models.CharField(max_length=50)
    ALL_data = models.CharField(max_length=1000)
    Amount = models.CharField(max_length=1000)


class Payment(models.Model):
    user_email = models.CharField(max_length=100, blank=True)
    bank_name = models.CharField(max_length=500)
    account_name = models.CharField(max_length=500)
    account_number = models.CharField(max_length=500)
    bank_code = models.CharField(max_length=500)
    purpose = models.CharField(max_length=500)
    Bill = models.CharField(max_length=500, default=0)
