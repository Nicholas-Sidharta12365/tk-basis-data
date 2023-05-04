from django.urls import path
from . import views
from listPertandingan.views import *

app_name = 'listPertandingan'

urlpatterns = [
    path('', index, name='listPertandingan'),
]