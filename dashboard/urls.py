from django.urls import path
from . import views
from dashboard.views import *

app_name = 'dashboard'

urlpatterns = [
    path('', index, name='dashboard'),
]