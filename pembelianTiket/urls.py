from django.urls import path
from . import views
from pembelianTiket.views import *

app_name = 'pembelianTiket'

urlpatterns = [
    path('', index, name='pembelianTiket'),
    path('waktu/', list_waktu, name='list_waktu'),
    path('waktu/pertandingan/', list_pertandingan, name='list_pertandingan'),
    path('waktu/pertandingan/buy/', beli_tiket, name='beli_tiket')
]