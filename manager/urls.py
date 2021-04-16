from django.urls import path
from .views import *
I = IndexDetail()
O = Output()

urlpatterns = [
    path('', Home, name='manager'),
    path('details/<web>', I.website_filter, name='managerD'),
    path('check', O.others, name='managerO'),
]

