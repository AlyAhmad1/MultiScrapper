from django.urls import path
from .views import form_data, reset_password
urlpatterns = [
    path('', form_data, name='wakanow_scraper'),
]
