from django.utils.timezone import now
from django.db import models


class JumaiaScraper(models.Model):
    user_email = models.CharField(max_length=100)
    All_Data = models.CharField(max_length=1000)
    Bill = models.CharField(max_length=100)
    paid_date = models.DateField(default=now)
