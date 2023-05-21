from django.urls import path
from . import views
from mulaiRapat.views import *

app_name = 'mulaiRapat'

urlpatterns = [
    path('', index, name='rapat'),
    path('isi/<uuid:id_pertandingan>/', pengisian_rapat, name='pengisian_rapat'),
    path('submit/<uuid:id_pertandingan>/<str:isi>/', submit_rapat,name='submit_rapat')
]