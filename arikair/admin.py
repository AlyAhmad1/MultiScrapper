from django.contrib import admin
from .models import RegUser, MailOTP, ArikData

# Register your models here.
admin.site.register(RegUser)
admin.site.register(MailOTP)
admin.site.register(ArikData)
