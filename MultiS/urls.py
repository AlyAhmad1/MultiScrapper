from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from wakanow import views
urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.register_user, name='signup'),
    path('login/', views.sign_in, name='login'),
    path('logout/', views.logout, name='logout'),
    path('admin/', admin.site.urls),
    path('wakanow/', include('wakanow.urls')),
    path('flyairspeace/', include('flyairpeace.urls')),
    path('arikair/', include('arikair.urls')),
    path('jumaia/', include('jumaia.urls')),
    path('manager/', include('manager.urls')),
    path('resetE/', views.reset_password_email, name='reset_email_enter'),
    path('reset/<int:email>', views.reset_password, name='reset_pass'),
    path('setpassword/<int:id>', views.set_new_password, name='set_new_pass'),
    path('payment/<int:Amount>/<path:ALLData>/<str:web>', views.payment, name='payment'),
    path('money_transfer', views.money_transfer, name='money_transfer'),
    path('test_transfer/', views.success_pay, name='test_transfer'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
