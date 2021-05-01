# Generated by Django 3.2 on 2021-04-29 23:58

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BeforePaymentData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=100)),
                ('web', models.CharField(max_length=50)),
                ('ALL_data', models.CharField(max_length=1000)),
                ('Account_data', models.CharField(max_length=1000)),
                ('Amount', models.CharField(max_length=1000)),
                ('Account', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='WakanowScrape',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_email', models.CharField(max_length=500)),
                ('passenger', models.CharField(max_length=500)),
                ('passenger_email', models.CharField(max_length=300)),
                ('details', models.CharField(max_length=300)),
                ('flight', models.CharField(max_length=300)),
                ('Total_Bill', models.CharField(max_length=300)),
                ('Amount_Paid', models.CharField(max_length=500)),
                ('Bill', models.CharField(default=0, max_length=500)),
                ('paid_date', models.DateField(default=datetime.datetime(2021, 4, 29, 23, 58, 39, 316118, tzinfo=utc))),
                ('bank_name', models.CharField(max_length=500)),
                ('account_name', models.CharField(max_length=500)),
                ('account_number', models.CharField(max_length=500)),
                ('bank_code', models.CharField(max_length=500)),
                ('purpose', models.CharField(max_length=500)),
            ],
        ),
    ]