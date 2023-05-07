from django.urls import path
from . import views
from mulaiRapat.views import *

app_name = 'mulaiRapat'

urlpatterns = [
    path('', index, name='mulaiRapat'),
    path('isi/', pengisian_rapat, name='pengisian_rapat')
]