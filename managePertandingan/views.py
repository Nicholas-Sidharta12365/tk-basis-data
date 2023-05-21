from django.conf import settings
import psycopg2
from django.shortcuts import render

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
    # params = [username, password]



    return render(request, 'manage.html')

def peristiwa(request):
    return render(request, 'peristiwa.html')
