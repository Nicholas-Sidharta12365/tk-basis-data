from django.shortcuts import render, redirect
from django.conf import settings
import psycopg2
import datetime
from pprint import pprint


# Create your views here.
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
    return render(request, 'index_create.html')

def add_pertandingan_index(request):
    user = request.session.get('logged_user')

    if user:
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
        table = 'panitia'

        fname = None
        lname = None
        phone = None
        email = None
        address = None
        role = None
        status = None
        rank = None
        meeting = None
        team_player_list = None
        upcoming_pertandingan_list = None

        current_datetime = datetime.datetime.now()

        query = '''
            SELECT MIN(Nama_Tim) as TimA, MAX(Nama_Tim) as TimB
            FROM sepak_bola.Tim_Pertandingan
            GROUP BY ID_Pertandingan
        '''
        

        params = [user['username']]
        cur.execute(query, params)
        result = cur.fetchall()

        context = {}
        cur.close()
        conn.close()


        context.update(get_role_context(role))

        return render(request, 'add_pertandingan_index.html')
    else:
        return redirect('/auth')

def list_waktu(request):
    return render(request, 'waktu.html')

def create_pertandingan(request):
    return render(request, 'create_pertandingan.html')

