from django.conf import settings
from django.shortcuts import render
import psycopg2

# Create your views here.
class Peminjaman:
    def __init__(self, nama_stadium, start_datetime):
        self.nama_stadium = nama_stadium
        self.start_datetime = start_datetime

class Stadium:
    def __init__(self, nama_stadium):
        self.nama_stadium = nama_stadium

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
    table_name = 'PEMINJAMAN'

    query_datetime = f"SELECT STADIUM.nama, {schema_name}.{table_name}.start_datetime FROM {schema_name}.STADIUM INNER JOIN {schema_name}.{table_name} ON {schema_name}.{table_name}.id_stadium={schema_name}.STADIUM.id_stadium;"
    cur.execute(query_datetime)
    
    result_datetime = cur.fetchall()
    peminjaman=[]
    for item in result_datetime:
        pinjam_stadium = Peminjaman(item[0],item[1])
        peminjaman.append(pinjam_stadium)
    
    context = {
                'peminjaman': peminjaman,
            }
    return render(request, 'peminjaman_stadium.html',context)

def cek_sesi(request):
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
    table_name = 'STADIUM'

    query = f"SELECT nama FROM {schema_name}.{table_name};"
    cur.execute(query)

    result = cur.fetchall()
    stadium=[]
    for item in result:
        nama_stadium = Stadium(item[0])
        stadium.append(nama_stadium)

    context = {
                'stadium': stadium,
            }
    print(context['stadium'])
    return render(request, 'cek_sesi.html',context)

def pesan_stadium(request):
    return render(request, 'pesan_stadium.html')