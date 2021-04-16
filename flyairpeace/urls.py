from django.urls import path, include
from .views import *
urlpatterns = [
    path('', form_data, name='flyairpeace_scraper'),
]

