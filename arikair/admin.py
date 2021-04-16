from django.contrib import admin
from .models import RegisteredUsers, MailOTP

# Register your models here.
admin.site.register(RegisteredUsers)
admin.site.register(MailOTP)


