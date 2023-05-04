from django.urls import path
from . import views
from historyRapat.views import *

app_name = 'historyRapat'

urlpatterns = [
    path('', index, name='historyRapat'),
]