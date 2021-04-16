from django.db import models


class ManagerData1(models.Model):
    website = models.CharField(max_length=100)
    Email = models.EmailField(null=True)     # sender_email
    form_data = models.BinaryField(max_length=1000)
    Scrape_Data = models.BinaryField(max_length=1000)

    def __str__(self):
        return self.website

