from django.shortcuts import render
from django.conf import settings
import psycopg2

def index(request):
    db_config = settings.DATABASES['default']

    conn = psycopg2.connect(
        dbname=db_config['NAME'],
        user=db_config['USER'],
        password=db_config['PASSWORD'],
        host=db_config['HOST'],
        port=db_config['PORT']
    )
    cur = conn.cursor()

    schema_name = 'sepak_bola'


    return render(request, 'mengelola.html')

def register_team(request):
    db_config = settings.DATABASES['default']

    conn = psycopg2.connect(
        dbname=db_config['NAME'],
        user=db_config['USER'],
        password=db_config['PASSWORD'],
        host=db_config['HOST'],
        port=db_config['PORT']
    )
    cur = conn.cursor()

    schema_name = 'sepak_bola'
    

    return render(request, 'register_team.html')

def register_player(request):

    return render(request, 'register_player.html')

def register_trainer(request):

    return render(request, 'register_trainer.html')