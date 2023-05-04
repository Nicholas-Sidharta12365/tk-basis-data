from django.urls import path
from . import views
from authentication.views import *

app_name = 'authentication'

urlpatterns = [
    path('', index, name='authentication'),
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    # path('logout/', logout, name='logout'),
]