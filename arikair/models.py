from django.utils.timezone import now
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_superuser(self, email, password, l_name, f_name, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Set is_staff True for superuser'))

        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Set is_superuser True for superuser'))

        return self.create_user(email, password, l_name, f_name, **extra_fields)

    def create_user(self, email, password, l_name, f_name, **extra_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(Email=email, FName=f_name, LName=l_name, **extra_fields)
        user.set_password(password)
        user.save()
        return user


class RegUser(AbstractBaseUser, PermissionsMixin):
    FName = models.CharField(max_length=50)
    LName = models.CharField(max_length=50)
    Email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'Email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.Email


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
