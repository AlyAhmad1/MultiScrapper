# Generated by Django 3.1.6 on 2021-04-13 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
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
                ('Email', models.EmailField(max_length=254, unique=True)),
                ('Password', models.CharField(max_length=10)),
            ],
        ),
    ]