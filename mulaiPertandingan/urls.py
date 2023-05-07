from django.urls import path
from . import views
from mulaiPertandingan.views import *

app_name = 'mulaiPertandingan'

urlpatterns = [
    path('', index, name='mulaiPertandingan'),
    path('addperistiwa/', add_peristiwa, name='add_peristiwa'),
]