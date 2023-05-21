import datetime
from django.shortcuts import redirect, render
from django.conf import settings
import psycopg2

def index(request):

    manajer_id = get_manajer_id(request)
    if manajer_id:
        rapat_participated = get_participated_rapat(manajer_id)
    else:
        return redirect('/')
    
    context = {
        'login_status': 'hidden',
        'register_status': 'hidden',
        'manage_pertandingan_status': 'hidden',
        'pembelian_tiket_status': 'hidden',
        'rapat_status': 'hidden',
        'pembuatan_pertandingan_status': 'hidden',
        'mulai_pertandingan_status': 'hidden',
        'rapat_participated': rapat_participated
    }
    return render(request, 'history.html', context)

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

def get_participated_rapat(manajer_id):
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
    table_rapat = 'Rapat'
    table_pertandingan = 'Pertandingan'
    table_stadium = 'Stadium'
    table_tim_pertandingan = 'Tim_Pertandingan'
    table_tim = 'Tim'
    table_tim_manajer = 'Tim_Manajer'
    current_datetime = datetime.datetime.now()

    query = f"""
            SELECT r.*, s.Nama AS Stadium_Name, tp1.Nama_Tim AS Nama_Tim_A, tp2.Nama_Tim AS Nama_Tim_B
            FROM {schema_name}.{table_rapat} AS r
            LEFT JOIN {schema_name}.{table_pertandingan} AS p ON r.ID_Pertandingan = p.ID_Pertandingan
            LEFT JOIN {schema_name}.{table_stadium} AS s ON p.Stadium = s.ID_Stadium
            LEFT JOIN {schema_name}.{table_tim_pertandingan} AS tp1 ON p.ID_Pertandingan = tp1.ID_Pertandingan
            LEFT JOIN {schema_name}.{table_tim_manajer} AS tm1 ON tp1.Nama_Tim = tm1.Nama_Tim AND tm1.ID_Manajer = %s
            LEFT JOIN {schema_name}.{table_tim_pertandingan} AS tp2 ON p.ID_Pertandingan = tp2.ID_Pertandingan
            LEFT JOIN {schema_name}.{table_tim_manajer} AS tm2 ON tp2.Nama_Tim = tm2.Nama_Tim AND tm2.ID_Manajer = %s
            LEFT JOIN {schema_name}.{table_tim} AS t1 ON tp1.Nama_Tim = t1.Nama_Tim
            LEFT JOIN {schema_name}.{table_tim} AS t2 ON tp2.Nama_Tim = t2.Nama_Tim
            WHERE (r.Manajer_Tim_A = %s OR r.Manajer_Tim_B = %s)
            AND p.Start_Datetime < %s
            AND tp1.Nama_Tim <> tp2.Nama_Tim
            """
    params = [manajer_id, manajer_id, manajer_id, manajer_id, current_datetime]
    cur.execute(query, params)
    result = cur.fetchall()
    cur.close()
    conn.close()

    return result
