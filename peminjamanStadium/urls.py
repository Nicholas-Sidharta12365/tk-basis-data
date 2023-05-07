from django.urls import path
from . import views
from peminjamanStadium.views import *

app_name = 'peminjamanStadium'

urlpatterns = [
    path('', index, name='peminjamanStadium'),
    path('sesi/', cek_sesi, name='cek_sesi'),
    path('sesi/pesan/', pesan_stadium, name='pesan_stadium')
]