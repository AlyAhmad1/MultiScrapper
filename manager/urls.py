from django.urls import path
from .views import *

urlpatterns = [
    path('', Home, name='manager'),
    path('details/<str:web>', details, name='all_data'),
    path('invoice/<int:id>/<str:web>', details_invoice, name='invoice'),
]

