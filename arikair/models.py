from django.db import models


class RegisteredUsers(models.Model):
    Email = models.EmailField(unique=True)
    Password = models.CharField(max_length=10)


class MailOTP(models.Model):
    Email = models.EmailField(primary_key=True)
    OTP = models.CharField(max_length=50)
    timestamp = models.DateTimeField(null=True)


class ArikData(models.Model):
    Pessenger = models.CharField(max_length=50)
    Flight = models.CharField(max_length=50)
    Departure = models.CharField(max_length=50)
    Destination = models.CharField(max_length=50)
    Date = models.CharField(max_length=50)
    Time = models.CharField(max_length=50)
    Seat = models.CharField(max_length=50, blank=True, null=True)
    Total_bagage = models.CharField(max_length=50)
    Tiket_fare = models.CharField(max_length=50)
    Tax = models.CharField(max_length=50)
    Surcharge = models.CharField(max_length=50)
    service = models.CharField(max_length=50)
    insurance_fee = models.CharField(max_length=50)
    Total_Amout_pay = models.IntegerField
