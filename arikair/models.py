from django.utils.timezone import now
from django.db import models


class RegisteredUsers(models.Model):
    FName = models.CharField(max_length=50)
    LName = models.CharField(max_length=50)
    Email = models.EmailField(unique=True)
    Password = models.CharField(max_length=10)


class MailOTP(models.Model):
    Email = models.EmailField(primary_key=True)
    OTP = models.CharField(max_length=50)
    timestamp = models.DateTimeField(null=True)


class ArikData(models.Model):
    user_email = models.CharField(max_length=100)
    Pessenger = models.CharField(max_length=50)
    Flight = models.CharField(max_length=50)
    Departure = models.CharField(max_length=50)
    Destination = models.CharField(max_length=50)
    Date = models.CharField(max_length=50)
    Time = models.CharField(max_length=50)
    Total_bagage = models.CharField(max_length=50)
    Tiket_fare = models.CharField(max_length=50)
    Tax = models.CharField(max_length=50)
    Surcharge = models.CharField(max_length=50)
    service = models.CharField(max_length=50)
    insurance_fee = models.CharField(max_length=50)
    Bill = models.CharField(max_length=50)
    paid_date = models.DateField(default=now)
    bank_name = models.CharField(max_length=500)
    account_name = models.CharField(max_length=500)
    account_number = models.CharField(max_length=500)
    bank_code = models.CharField(max_length=500)
    purpose = models.CharField(max_length=500)
