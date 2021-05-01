# Generated by Django 3.2 on 2021-04-29 23:58

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ArikData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_email', models.CharField(max_length=100)),
                ('Pessenger', models.CharField(max_length=50)),
                ('Flight', models.CharField(max_length=50)),
                ('Departure', models.CharField(max_length=50)),
                ('Destination', models.CharField(max_length=50)),
                ('Date', models.CharField(max_length=50)),
                ('Time', models.CharField(max_length=50)),
                ('Total_bagage', models.CharField(max_length=50)),
                ('Tiket_fare', models.CharField(max_length=50)),
                ('Tax', models.CharField(max_length=50)),
                ('Surcharge', models.CharField(max_length=50)),
                ('service', models.CharField(max_length=50)),
                ('insurance_fee', models.CharField(max_length=50)),
                ('Bill', models.CharField(max_length=50)),
                ('paid_date', models.DateField(default=django.utils.timezone.now)),
                ('bank_name', models.CharField(max_length=500)),
                ('account_name', models.CharField(max_length=500)),
                ('account_number', models.CharField(max_length=500)),
                ('bank_code', models.CharField(max_length=500)),
                ('purpose', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='MailOTP',
            fields=[
                ('Email', models.EmailField(max_length=254, primary_key=True, serialize=False)),
                ('OTP', models.CharField(max_length=50)),
                ('timestamp', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='RegisteredUsers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('FName', models.CharField(max_length=50)),
                ('LName', models.CharField(max_length=50)),
                ('Email', models.EmailField(max_length=254, unique=True)),
                ('Password', models.CharField(max_length=10)),
            ],
        ),
    ]
