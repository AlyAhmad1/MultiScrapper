from django.urls import path
from .views import *

urlpatterns = [
    path('', form_data, name='arikair_scraper'),
]
