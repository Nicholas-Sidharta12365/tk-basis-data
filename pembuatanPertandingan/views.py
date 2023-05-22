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

        # query = f"SELECT * FROM {schema_name}.{table}"

        # query = '''
        #             SELECT Ta.Nama_Tim, Tb.Nama_Tim
        #             FROM sepak_bola.Tim_Pertandingan M
        #             JOIN sepak_bola.Tim_Pertandingan Ta ON Ta.Nama_Tim = M.Nama_Tim AND Ta.ID_Pertandingan = M.ID_Pertandingan
        #             JOIN sepak_bola.Tim_Pertandingan Tb ON Tb.Nama_Tim = M.Nama_Tim AND Tb.ID_Pertandingan = M.ID_Pertandingan
        #             WHERE
        #             Ta.Nama_Tim < Tb.Nama_Tim
        #             AND Ta.Nama_Tim = M.Nama_Tim AND Ta.ID_Pertandingan = M.ID_Pertandingan
        #             AND Tb.Nama_Tim = M.Nama_Tim AND Tb.ID_Pertandingan = M.ID_Pertandingan
        #         '''
        # query = '''
        #             WITH cte AS (
        #                 SELECT *, ROW_NUMBER() OVER (PARTITION BY ID_Pertandingan ORDER BY Nama_Tim) rn
        #                 FROM Tim_Pertandingan
        #             )

        #             SELECT
        #                 ID_Pertandingan
        #                 MAX(CASE WHEN rn = 1 THEN Nama_Tim END) AS Col1,
        #                 MAX(CASE WHEN rn = 2 THEN Nama_Tim END) AS Col2,
        #             FROM cte
        #             GROUP BY ID_Pertandingan
        #             ORDER BY ID_Pertandingan
        #         '''
        query = '''
                    SELECT MIN(Nama_Tim) as TimA, MAX(Nama_Tim) as TimB
                    FROM sepak_bola.Tim_Pertandingan
                    GROUP BY ID_Pertandingan
                '''
        

        params = [user['username']]
        cur.execute(query, params)
        result = cur.fetchall() # Grup A

        context = {}
        grup_b = []
        grup_c = []
        grup_d = []
        if result:
            role = table
            # context["teams": result]
            context.update({"grup_a": result})
            context.update({"grup_b": grup_b})
            context.update({"grup_c": grup_c})
            context.update({"grup_d": grup_d})

            if (len(result) > len(grup_b)):
                context.update({"ab_range":range(len(result))})
            else:
                context.update({"ab_range":range(len(grup_b))})
            print(f"User is: {user}")
            # pprint(result)


        cur.close()
        conn.close()


        context.update(get_role_context(role))
        # print(context)

        return render(request, 'index_create.html', context)
    else:
        return redirect('/auth')

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

