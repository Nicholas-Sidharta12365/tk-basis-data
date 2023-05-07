from django.urls import path
from . import views
from managePertandingan.views import *

app_name = 'managePertandingan'

urlpatterns = [
    path('', index, name='managePertandingan'),
    path('peristiwa/', peristiwa, name='peristiwa'),
]