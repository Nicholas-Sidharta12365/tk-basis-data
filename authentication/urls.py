from django.urls import path
from . import views
from authentication.views import *

app_name = 'authentication'

urlpatterns = [
    path('', index, name='authentication'),
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('register/user/', register_user, name='register_user'),
    path('register/manajer/', register_manajer, name='register_manajer'),
    path('register/penonton/', register_penonton, name='register_penonton'),
    path('register/panitia/', register_panitia, name='register_panitia'),
    path('logout/', logout, name='logout'),
]