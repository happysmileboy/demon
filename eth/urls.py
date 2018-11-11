from django.urls import path
from . import views
app_name = 'eth'

urlpatterns = [
    path('create_adminwallet', views.create_adminwallet, name='create_adminwallet'),
    path('create_wallet', views.create_wallet, name='create_wallet'),
    path('my_wallet', views.my_wallet, name='my_wallet'),
]
