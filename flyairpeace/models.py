from django.utils.timezone import now
from django.db import models

# Create your models here.


class AirpeaceScraper(models.Model):
    user_email = models.CharField(max_length=100)
    passenger = models.CharField(max_length=50)
    Bill = models.CharField(max_length=100)
    paid_date = models.DateField(default=now)
