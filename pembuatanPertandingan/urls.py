from django.urls import path
from . import views
from pembuatanPertandingan.views import *

app_name = 'pembuatanPertandingan'

urlpatterns = [
    path('', index, name='pembuatanPertandingan'),
    path('add/', add_pertandingan_index, name='add_pertandingan_index'),
    path('add/waktu/', list_waktu, name='list_waktu'),
    path('add/waktu/create/', create_pertandingan, name='create_pertandingan'),

]