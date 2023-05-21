from django.conf import settings
from django.shortcuts import render
import psycopg2

# Create your views here.
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
    table_name = 'USER_SYSTEM'

    query = f"SELECT * FROM {schema_name}.{table_name} WHERE username = %s AND password = %s;"
    return render(request, 'index_create.html')

def add_pertandingan_index(request):
    return render(request, 'add_pertandingan_index.html')

def list_waktu(request):
    return render(request, 'waktu.html')

def create_pertandingan(request):
    return render(request, 'create_pertandingan.html')

