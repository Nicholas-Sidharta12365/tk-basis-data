from django.shortcuts import render
from django.conf import settings
import psycopg2
from datetime import datetime

def index(request):
    role = request.session.get('logged_user')['role']

    if role == 'penonton':
        pertandingan_list = get_upcoming_pertandingan()
        context = {
            'login_status': 'hidden',
            'register_status': 'hidden',
            'pertandingan_list': pertandingan_list,
            'mengelola_tim_status': 'hidden',
            'peminjaman_stadium_status': 'hidden',
            'manage_pertandingan_status': 'hidden',
            'rapat_status': 'hidden',
            'history_rapat_status': 'hidden',
            'pembuatan_pertandingan_status': 'hidden',
            'mulai_pertandingan_status': 'hidden'
        }
    elif role == 'manajer':
        manager_id = get_manajer_id(request)
        pertandingan_list = get_upcoming_pertandingan_manajer(manager_id)
        context = {
            'login_status': 'hidden',
            'register_status': 'hidden',
            'pertandingan_list': pertandingan_list,
            'manage_pertandingan_status': 'hidden',
            'pembelian_tiket_status': 'hidden',
            'rapat_status': 'hidden',
            'pembuatan_pertandingan_status': 'hidden',
            'mulai_pertandingan_status': 'hidden'
        }
    else:
        pertandingan_list = []
        context = {}


    return render(request, 'list.html', context)

def get_upcoming_pertandingan():
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
    table_pertandingan = 'Pertandingan'
    table_stadium = 'Stadium'
    table_tim_pertandingan = 'Tim_Pertandingan'

    current_datetime = datetime.now()

    query = f"""
        SELECT tp1.Nama_Tim AS Nama_Tim_A, tp2.Nama_Tim AS Nama_Tim_B, s.Nama AS Stadium, p.Start_Datetime
        FROM {schema_name}.{table_pertandingan} AS p
        LEFT JOIN {schema_name}.{table_stadium} AS s ON p.Stadium = s.ID_Stadium
        LEFT JOIN {schema_name}.{table_tim_pertandingan} AS tp1 ON p.ID_Pertandingan = tp1.ID_Pertandingan
        LEFT JOIN {schema_name}.{table_tim_pertandingan} AS tp2 ON p.ID_Pertandingan = tp2.ID_Pertandingan
        WHERE p.Start_Datetime > %s
        AND tp1.Nama_Tim <> tp2.Nama_Tim
        ORDER BY p.Start_Datetime ASC;

    """
    params = [current_datetime]
    cur.execute(query, params)
    result = cur.fetchall()
    cur.close()
    conn.close()

    return result

def get_upcoming_pertandingan_manajer(manajer_id):
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
    table_pertandingan = 'Pertandingan'
    table_stadium = 'Stadium'
    table_tim_pertandingan = 'Tim_Pertandingan'
    table_tim_manajer = 'Tim_Manajer'

    current_datetime = datetime.now()

    query = f"""
            SELECT tp1.Nama_Tim AS Nama_Tim_A, tp2.Nama_Tim AS Nama_Tim_B, s.Nama AS Stadium, p.Start_Datetime
            FROM {schema_name}.{table_pertandingan} AS p
            LEFT JOIN {schema_name}.{table_stadium} AS s ON p.Stadium = s.ID_Stadium
            LEFT JOIN {schema_name}.{table_tim_pertandingan} AS tp1 ON p.ID_Pertandingan = tp1.ID_Pertandingan
            LEFT JOIN {schema_name}.{table_tim_manajer} AS tm1 ON tp1.Nama_Tim = tm1.Nama_Tim
            LEFT JOIN {schema_name}.{table_tim_pertandingan} AS tp2 ON p.ID_Pertandingan = tp2.ID_Pertandingan
            LEFT JOIN {schema_name}.{table_tim_manajer} AS tm2 ON tp2.Nama_Tim = tm2.Nama_Tim
            WHERE p.Start_Datetime > %s
            AND tp1.Nama_Tim <> tp2.Nama_Tim
            AND (tm1.ID_Manajer = %s
            OR tm2.ID_Manajer = %s)
            ORDER BY p.Start_Datetime ASC;
            """

    params = [current_datetime, manajer_id, manajer_id]
    cur.execute(query, params)
    result = cur.fetchall()
    cur.close()
    conn.close()

    return result

def get_manajer_id(request):
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
    table = 'Manajer'

    username = request.session.get('logged_user')['username']
    query = f"SELECT * FROM {schema_name}.{table} WHERE username = %s"
    params = [username]
    cur.execute(query, params)
    result = cur.fetchall()

    if result:
        cur.close()
        conn.close()
        return result[0][0]
    else:
        cur.close()
        conn.close()
        return None