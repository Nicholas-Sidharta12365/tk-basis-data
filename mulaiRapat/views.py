import datetime
from http.client import HTTPResponse
from django.shortcuts import render
from django.conf import settings
import psycopg2

# Create your views here.
class List_Pinjam:
    def __init__(self, tim, start_datetime, end_datetime, stadium, id_pertandingan):
        self.tim = tim
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime
        self.stadium = stadium
        self.id_pertandingan = id_pertandingan

class Isi_Rapat:
    def __init__(self, id_pertandingan, datetime, id_panitia, id_manajer_a, id_manajer_b, nama_a, nama_b):
        self.id_pertandingan = id_pertandingan
        self.datetime = datetime
        self.id_panitia = id_panitia
        self.id_manajer_a = id_manajer_a
        self.id_manajer_b = id_manajer_b
        self.nama_a = nama_a
        self.nama_b = nama_b

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

    query_tim = f"SELECT * FROM (\
                    SELECT ROW_NUMBER() OVER(ORDER BY t2.id_pertandingan), t.nama_tim|| ' vs ' || t2.nama_tim,\
                          p.start_datetime, p.end_datetime, s.nama, t.id_pertandingan\
                    FROM {schema_name}.TIM_PERTANDINGAN t \
                        INNER JOIN {schema_name}.TIM_PERTANDINGAN t2\
                            ON t2.id_pertandingan=t.id_pertandingan AND t2.nama_tim!=t.nama_tim\
                        INNER JOIN {schema_name}.PERTANDINGAN p \
                            ON p.id_pertandingan=t.id_pertandingan\
                        INNER JOIN  {schema_name}.STADIUM s\
                            ON p.stadium=s.id_stadium\
                ) x\
                                WHERE MOD(x.row_number,2)=0;"
    cur.execute(query_tim)
    
    result_tim = cur.fetchall()
    list_peminjaman=[]
    for item in result_tim:
        pinjam_stadium = List_Pinjam(item[1],item[2],item[3],item[4],item[5])
        list_peminjaman.append(pinjam_stadium)
    
    context = {
                'list_peminjaman': list_peminjaman,
            }
    context.update(get_role_context('panitia'))
    return render(request, 'index_rapat.html',context)

def pengisian_rapat(request, id_pertandingan):
    db_config = settings.DATABASES['default']

    conn = psycopg2.connect(
            dbname=db_config['NAME'],
            user=db_config['USER'],
            password=db_config['PASSWORD'],
            host=db_config['HOST'],
            port=db_config['PORT']
        )
    cur = conn.cursor()
    id=id_pertandingan
    query = f"SELECT tm.id_manajer, tm.nama_tim\
                FROM sepak_bola.tim_manajer tm\
                INNER JOIN sepak_bola.tim_pertandingan tp\
                    ON tp.nama_tim=tm.nama_tim\
                WHERE tp.id_pertandingan='{id}';"
    cur.execute(query)
    result = cur.fetchall()
    current_datetime = datetime.datetime.now() 
    user = request.session.get('logged_user')
    username = user['username']
    query_id_panitia = f"SELECT id_panitia\
                            FROM sepak_bola.PANITIA\
                                WHERE username='{username}';"
    cur.execute(query_id_panitia)
    result_id_panitia = cur.fetchall()
    detail = Isi_Rapat(id_pertandingan, current_datetime,result_id_panitia,result[0][0],result[1][0],result[0][1],result[1][1])  

    print(detail.id_pertandingan)
    context = {
                'detail_rapat': detail,
            } 
    context.update(get_role_context('panitia'))
    return render(request, 'pengisian_rapat.html',context)

def submit_rapat(request, id_pertandingan, isi):
    db_config = settings.DATABASES['default']

    conn = psycopg2.connect(
            dbname=db_config['NAME'],
            user=db_config['USER'],
            password=db_config['PASSWORD'],
            host=db_config['HOST'],
            port=db_config['PORT']
        )
    cur = conn.cursor()
    id=id_pertandingan
    query = f"SELECT tm.id_manajer, tm.nama_tim\
                FROM sepak_bola.tim_manajer tm\
                INNER JOIN sepak_bola.tim_pertandingan tp\
                    ON tp.nama_tim=tm.nama_tim\
                WHERE tp.id_pertandingan='{id}';"
    cur.execute(query)
    result = cur.fetchall()
    current_datetime = datetime.datetime.now() 
    user = request.session.get('logged_user')
    username = user['username']
    query_id_panitia = f"SELECT id_panitia\
                            FROM sepak_bola.PANITIA\
                                WHERE username='{username}';"
    cur.execute(query_id_panitia)
    result_id_panitia = cur.fetchall()
    detail = Isi_Rapat(id_pertandingan, current_datetime,result_id_panitia,result[0][0],result[1][0],result[0][1],result[1][1]) 
    id_panitia = str(detail.id_panitia[0][0])
    query_insert_rapat =  f"INSERT INTO sepak_bola.RAPAT (id_pertandingan,datetime,perwakilan_panitia,manajer_tim_a,manajer_tim_b,isi_rapat)\
                            VALUES ('{detail.id_pertandingan}','{detail.datetime}',\
                                '{id_panitia}','{detail.id_manajer_a}','{detail.id_manajer_b}',\
                                    '{isi}');"
    cur.execute(query_insert_rapat)
    return render(request, 'index_rapat.html')