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

def get_role_context(role):
    context = {
        'role': role,
        'login_status': 'hidden',
        'register_status': 'hidden',
        'dashboard_status': None,
        'mengelola_tim_status': None,
        'peminjaman_stadium_status': None,
        'manage_pertandingan_status': None,
        'pembelian_tiket_status': None,
        'list_pertandingan_status': None,
        'rapat_status': None,
        'history_rapat_status': None,
        'pembuatan_pertandingan_status': None,
        'mulai_pertandingan_status': None
    }

    if role == 'manajer':
        context.update({
            'manage_pertandingan_status': 'hidden',
            'pembelian_tiket_status': 'hidden',
            'rapat_status': 'hidden',
            'pembuatan_pertandingan_status': 'hidden',
            'mulai_pertandingan_status': 'hidden'
        })
    elif role == 'penonton':
        context.update({
            'mengelola_tim_status': 'hidden',
            'peminjaman_stadium_status': 'hidden',
            'manage_pertandingan_status': 'hidden',
            'rapat_status': 'hidden',
            'history_rapat_status': 'hidden',
            'pembuatan_pertandingan_status': 'hidden',
            'mulai_pertandingan_status': 'hidden'
        })
    elif role == 'panitia':
        context.update({
            'mengelola_tim_status': 'hidden',
            'peminjaman_stadium_status': 'hidden',
            'pembelian_tiket_status': 'hidden',
            'list_pertandingan_status': 'hidden',
            'history_rapat_status': 'hidden',
            'pembuatan_pertandingan_status': 'hidden',
            'mulai_pertandingan_status': 'hidden'
        })

    return context

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
    context.update(get_role_context('manajer'))
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
    context.update(get_role_context('manajer'))
    return render(request, 'cek_sesi.html',context)

def pesan_stadium(request):
    context = {}
    context.update(get_role_context('manajer'))
    return render(request, 'pesan_stadium.html',context)