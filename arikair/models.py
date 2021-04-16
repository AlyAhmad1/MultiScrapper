from django.db import models


class RegisteredUsers(models.Model):
    Email = models.EmailField(unique=True)
    Password = models.CharField(max_length=10)


class MailOTP(models.Model):
    Email = models.EmailField(primary_key=True)
    OTP = models.CharField(max_length=50)
    timestamp = models.DateTimeField(null=True)

