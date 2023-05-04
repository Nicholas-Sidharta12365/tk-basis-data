from django.urls import path
from . import views
from mengelolaTim.views import *

app_name = 'mengelolaTim'

urlpatterns = [
    path('', index, name='mengelolaTim'),
    path('form/', register_team, name='register_team'),
    path('player/', register_player, name='register_player'),
    path('trainer/', register_trainer, name='register_trainer'),
]