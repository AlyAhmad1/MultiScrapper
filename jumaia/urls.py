from django.urls import path
from .views import *

urlpatterns = [
    # path('data/delete/<index>/<path:whole>/<T>', data_update, name='jumaia_scraper1_del'),
    path('submit/', submit_data, name='jumaia_scraper1_del') # ajax view
]
