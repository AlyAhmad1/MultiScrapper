from django.contrib import admin
from .models import RegisteredUsers, MailOTP, ArikData

# Register your models here.
admin.site.register(RegisteredUsers)
admin.site.register(MailOTP)
admin.site.register(ArikData)
