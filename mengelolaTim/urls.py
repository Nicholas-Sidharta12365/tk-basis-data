from django.urls import path
from . import views
from mengelolaTim.views import *

app_name = 'mengelolaTim'

urlpatterns = [
    path('', index, name='mengelolaTim'),
    path('form/', register_team, name='register_team'),
    path('player/', register_player, name='register_player'),
    path('trainer/', register_trainer, name='register_trainer'),
    path('make_captain/', make_captain, name='make_captain'),
    path('delete_pemain/', delete_pemain, name='delete_pemain'),
    path('delete_pelatih/', delete_pelatih, name='delete_pelatih'),
    # path to register player
    path('register_player/', register_player, name='register_player'),
    # path to register trainer
    path('register_trainer/', register_trainer, name='register_trainer'),
    # path to register team
    path('register_team/', register_team, name='register_team'),
]