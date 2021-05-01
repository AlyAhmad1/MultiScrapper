from django.urls import path
from .views import *

urlpatterns = [
    path('', form_data, name='jumaia_scraper'),
    path('data', All_data, name='jumaia_scraper1'),
    path('data/delete/<index>/<path:whole>/<T>', data_update, name='jumaia_scraper1_del'),
]
