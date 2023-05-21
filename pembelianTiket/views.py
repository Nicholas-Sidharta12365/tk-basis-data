from django.shortcuts import redirect, render
from django.conf import settings
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

    query = f"SELECT ID_Stadium, Nama FROM {schema_name}.Stadium"
    cur.execute(query)
    stadiums = [{'ID_Stadium': row[0], 'Nama': row[1]} for row in cur.fetchall()]
    context = {
        'stadiums': stadiums,
        'login_status': 'hidden',
        'register_status': 'hidden',
        'mengelola_tim_status': 'hidden',
        'peminjaman_stadium_status': 'hidden',
        'manage_pertandingan_status': 'hidden',
        'rapat_status': 'hidden',
        'history_rapat_status': 'hidden',
        'pembuatan_pertandingan_status': 'hidden',
        'mulai_pertandingan_status': 'hidden'
        }
    
    cur.close()
    conn.close()

    return render(request, 'index_pembelian_tiket.html', context)

def list_waktu(request):
    stadium_id = request.GET.get('stadium')
    tanggal = request.GET.get('tanggal')
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

    query = f"SELECT DISTINCT Start_Datetime, End_Datetime FROM {schema_name}.Pertandingan WHERE Stadium = %s AND Start_Datetime >= %s"
    cur.execute(query, [stadium_id, tanggal])
    pertandingan_dates = [{'Start_Datetime': row[0], 'End_Datetime': row[1]} for row in cur.fetchall()]

    context = {
            'stadium_id': stadium_id,
            'dates': pertandingan_dates,
            'login_status': 'hidden',
            'register_status': 'hidden',
            'mengelola_tim_status': 'hidden',
            'peminjaman_stadium_status': 'hidden',
            'manage_pertandingan_status': 'hidden',
            'rapat_status': 'hidden',
            'history_rapat_status': 'hidden',
            'pembuatan_pertandingan_status': 'hidden',
            'mulai_pertandingan_status': 'hidden'
            }
        
    cur.close()
    conn.close()

    return render(request, 'list_waktu.html', context)

def list_pertandingan(request):
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

    # Retrieve URL parameters
    stadium_id = request.GET.get('stadium')
    date_start = request.GET.get('dateStart')  # May 5, 2023, 11 a.m.
    date_end = request.GET.get('dateEnd')

    # Split the date string by comma and extract the relevant parts for date_start
    date_parts_start = date_start.split(", ")
    month_start, day_start = date_parts_start[0].split()
    year_time_start = date_parts_start[1]
    year_start = year_time_start.split()[0]
    time_start = date_parts_start[2]

    # Split the date string by comma and extract the relevant parts for date_end
    date_parts_end = date_end.split(", ")
    month_end, day_end = date_parts_end[0].split()
    year_time_end = date_parts_end[1]
    year_end = year_time_end.split()[0]
    time_end = date_parts_end[2]

    # Convert month name to month number for date_start
    month_mapping = {
        'January': '01',
        'February': '02',
        'March': '03',
        'April': '04',
        'May': '05',
        'June': '06',
        'July': '07',
        'August': '08',
        'September': '09',
        'October': '10',
        'November': '11',
        'December': '12'
    }
    month_number_start = month_mapping[month_start]

    # Convert month name to month number for date_end
    month_number_end = month_mapping[month_end]

    # Format time_start
    time_parts_start = time_start.split()
    hour_start = int(time_parts_start[0])
    if time_parts_start[1] == 'p.m.':
        hour_start += 12
    formatted_time_start = f"{hour_start:02d}:00:00"

    # Format time_end
    time_parts_end = time_end.split()
    hour_end = int(time_parts_end[0])
    if time_parts_end[1] == 'p.m.':
        hour_end += 12
    formatted_time_end = f"{hour_end:02d}:00:00"

    # Construct the desired format for date_start
    formatted_date_start = f"{year_start}/{month_number_start}/{day_start} {formatted_time_start}"

    # Construct the desired format for date_end
    formatted_date_end = f"{year_end}/{month_number_end}/{day_end} {formatted_time_end}"

    query = f"SELECT ID_Pertandingan FROM {schema_name}.Pertandingan WHERE Stadium = %s AND Start_Datetime >= %s AND End_Datetime <= %s"
    params = (stadium_id, formatted_date_start, formatted_date_end)
    cur.execute(query, params)
    pertandingan_ids = [row[0] for row in cur.fetchall()]

    # Query to retrieve Tim from Tim_Pertandingan based on ID_Pertandingan
    query = f"SELECT Nama_Tim FROM {schema_name}.Tim_Pertandingan WHERE ID_Pertandingan IN %s"
    cur.execute(query, (tuple(pertandingan_ids),))
    tim_pertandingan = cur.fetchall()

    # Process the results to create a list of dictionaries with team_a and team_b
    counter = 0
    pertandingan_list = []
    for i in range(len(tim_pertandingan)):
        if i % 2 == 0:
            pertandingan_list.append({
                'id_team': pertandingan_ids[counter], 
                'team_a': tim_pertandingan[i][0],
                'team_b': ''
            })
            counter += 1
        else:
            pertandingan_list[-1]['team_b'] = tim_pertandingan[i][0]

    context = {
        'login_status': 'hidden',
        'register_status': 'hidden',
        'mengelola_tim_status': 'hidden',
        'peminjaman_stadium_status': 'hidden',
        'manage_pertandingan_status': 'hidden',
        'rapat_status': 'hidden',
        'history_rapat_status': 'hidden',
        'pembuatan_pertandingan_status': 'hidden',
        'mulai_pertandingan_status': 'hidden',
        'pertandingan_list': pertandingan_list
    }

    cur.close()
    conn.close()

    return render(request, 'list_pertandingan.html', context)

def beli_tiket(request):
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

    if request.method == 'POST':
        nomor_receipt = generate_receipt_number()
        id_penonton = get_penonton_id(request)
        jenis_tiket = request.POST.get('jenis_tiket')
        jenis_pembayaran = request.POST.get('jenis_pembayaran')
        id_pertandingan = request.GET.get('pertandingan')

        # Insert data into the Pembelian_Tiket table
        insert_query = f"INSERT INTO {schema_name}.Pembelian_Tiket (Nomor_Receipt, id_penonton, Jenis_Tiket, Jenis_Pembayaran, id_pertandingan) " \
                       "VALUES (%s, %s, %s, %s, %s)"
        values = (nomor_receipt, id_penonton, jenis_tiket, jenis_pembayaran, id_pertandingan)
        cur.execute(insert_query, values)
        conn.commit()
        cur.close()
        conn.close()

        return redirect('/dashboard')

    cur.close()
    conn.close()

    context = {
        'login_status': 'hidden',
        'register_status': 'hidden',
        'mengelola_tim_status': 'hidden',
        'peminjaman_stadium_status': 'hidden',
        'manage_pertandingan_status': 'hidden',
        'rapat_status': 'hidden',
        'history_rapat_status': 'hidden',
        'pembuatan_pertandingan_status': 'hidden',
        'mulai_pertandingan_status': 'hidden'
    }

    return render(request, 'beli_tiket.html', context)

def generate_receipt_number():
    import random
    receipt_number = ''.join(random.choice('0123456789') for _ in range(15))
    return receipt_number

def get_penonton_id(request):
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

    username = request.session.get('logged_user')['username']
    schema_name = 'sepak_bola'
    table = 'Penonton'
    
    query = f"SELECT * FROM {schema_name}.{table} WHERE username = %s"
    params = [username]
    cur.execute(query, params)
    result = cur.fetchall()

    if result:
        return result[0][0] 
    else:
        return None