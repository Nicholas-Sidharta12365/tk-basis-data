from django.shortcuts import render, redirect
from django.conf import settings
import psycopg2
import datetime
from pprint import pprint
import uuid


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
        query_insert = ""
        
        if request.method == 'POST':
            wasit_utama = request.POST.get('wasitUtama')
            wasit_pembantu_1 = request.POST.get('wasitPembantu1')
            wasit_pembantu_2 = request.POST.get('wasitPembantu2')
            wasit_cadangan = request.POST.get('wasitCadangan')
            tim_satu = request.POST.get('timSatu')
            tim_dua = request.POST.get('timDua')
            stadium_id = request.POST.get('stadiumId')
            tanggal = request.POST.get('tanggal')
            generated_uuid = uuid.uuid4()
            uuid_string = str(generated_uuid)

            # print('stadium: ' + stadium_id)
            # print('tanggal: ' + tanggal)
            # print('wasit utama: ' + wasit_utama)
            # print('wasit pembantu 1: ' + wasit_pembantu_1)
            # print('wasit pembantu 2: ' + wasit_pembantu_2)
            # print('wasit cadangan: ' + wasit_cadangan)

            query_insert = f"INSERT INTO sepak_bola.Pertandingan (id_pertandingan, start_datetime, end_datetime, stadium) VALUES ('{uuid_string}', '{tanggal} 14:00:00', '{tanggal} 16:00:00', '{stadium_id}')"
            cur.execute(query_insert)
            query_update_tim_satu = f"INSERT INTO sepak_bola.Tim_Pertandingan VALUES ('{tim_satu}', '{uuid_string}', '0-0')"
            query_update_tim_dua = f"INSERT INTO sepak_bola.Tim_Pertandingan VALUES ('{tim_dua}', '{uuid_string}', '0-0')"
            query_update_wasit_utama = f"INSERT INTO sepak_bola.Wasit_Bertugas VALUES ('{wasit_utama}', '{uuid_string}', 'wasit utama')"
            query_update_wasit_pembantu_1 = f"INSERT INTO sepak_bola.Wasit_Bertugas VALUES ('{wasit_pembantu_1}', '{uuid_string}', 'hakim garis')"
            query_update_wasit_pembantu_2 = f"INSERT INTO sepak_bola.Wasit_Bertugas VALUES ('{wasit_pembantu_2}', '{uuid_string}', 'hakim garis')"
            query_update_wasit_cadangan = f"INSERT INTO sepak_bola.Wasit_Bertugas VALUES ('{wasit_cadangan}', '{uuid_string}', 'wasit cadangan')"
            cur.execute(query_update_tim_satu)
            cur.execute(query_update_tim_dua)
            cur.execute(query_update_wasit_utama)
            cur.execute(query_update_wasit_pembantu_1)
            cur.execute(query_update_wasit_pembantu_2)
            cur.execute(query_update_wasit_cadangan)
            
            

        current_datetime = datetime.datetime.now()

        query = '''
                    SELECT MIN(Nama_Tim) as TimA, MAX(Nama_Tim) as TimB, id_pertandingan
                    FROM sepak_bola.Tim_Pertandingan
                    GROUP BY ID_Pertandingan
                '''
        
        # if query_insert:
        #     params = [user['username']]
        #     cur.execute(query_insert)
        

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
            # print(f"User is: {user}")
            # pprint(result)


        conn.commit()
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
            SELECT S.nama, S.id_stadium
            FROM sepak_bola.Stadium S
        '''
        

        params = [user['username']]
        cur.execute(query, params)
        result = cur.fetchall()

        context = {}

        if result:
            role = table
            context.update({"stadium": result})
            # pprint(result)
        cur.close()
        conn.close()


        context.update(get_role_context(role))
        # print(context)

        return render(request, 'add_pertandingan_index.html', context)
    else:
        return redirect('/auth')

def list_waktu(request):
    if request.method == 'POST':
        stadium = request.POST.get('stadium')
        tanggal = request.POST.get('tanggal')
        # print(stadium)
        # print(tanggal)
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
                        SELECT P.id_pertandingan, P.stadium
                        FROM sepak_bola.Pertandingan P
                    '''
            

            params = [user['username']]
            cur.execute(query, params)
            result = cur.fetchall()
            context = {}
            if result:
                role = table
                context.update({"tes": result})


            cur.close()
            conn.close()


            context.update(get_role_context(role))
            return render(request, 'waktu.html', context)
        else:
            return redirect('/auth')
    else:
        return redirect('/creation')






def create_pertandingan(request):
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
        role = table
        status = None
        rank = None
        meeting = None
        team_player_list = None
        upcoming_pertandingan_list = None

        current_datetime = datetime.datetime.now()


        context = {}


        stadium_id = request.POST.get('stadium')
        tanggal = request.POST.get('tanggal')

        if ((stadium_id is None) or tanggal is None):
            return redirect ('/creation')

        if request.method == 'POST':
            stadium_id = request.POST.get('stadium')
            tanggal = request.POST.get('tanggal')
            context.update({"stadium_id": stadium_id})
            context.update({"tanggal": tanggal})

            query_wasit = '''
                        SELECT W.ID_Wasit, NP.Nama_Depan, NP.Nama_Belakang
                        FROM sepak_bola.Wasit W, sepak_bola.Non_Pemain NP
                        WHERE NP.ID = W.ID_Wasit
                    '''

            params = [user['username']]
            cur.execute(query_wasit, params)
            result = cur.fetchall()
            if result:
                role = table
                context.update({"wasit": result})
            
            query_tim = '''
                        SELECT T.Nama_Tim
                        FROM sepak_bola.Tim T
                    '''
            params = [user['username']]
            cur.execute(query_tim, params)
            result = cur.fetchall()
            if result:
                role = table
                context.update({"tim": result})

        # pprint(context.get('wasit'))
        # pprint(len(context.get('wasit')))

        # pprint(context.get('tim'))
        # pprint(len(context.get('tim')))
        

        cur.close()
        conn.close()
        context.update(get_role_context(role))


        return render(request, 'create_pertandingan.html', context)
    else:
        return redirect('/auth')


def delete_pertandingan(request):
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
        context = {}

        if request.method == 'POST':
            idPertandingan = request.POST.get('idPertandingan')
            query_delete_pertandingan = f"DELETE FROM sepak_bola.Pertandingan WHERE id_pertandingan='{idPertandingan}'"
            query_delete_tim_pertandingan = f"DELETE FROM sepak_bola.Tim_Pertandingan WHERE id_pertandingan='{idPertandingan}'"
            query_delete_wasit_pertandingan = f"DELETE FROM sepak_bola.Wasit_Bertugas WHERE id_pertandingan='{idPertandingan}'"
            cur.execute(query_delete_wasit_pertandingan)
            cur.execute(query_delete_tim_pertandingan)
            cur.execute(query_delete_pertandingan)
        conn.commit()
        cur.close()
        conn.close()


        context.update(get_role_context(role))
        # print(context)

        return redirect('/creation')
    else:
        return redirect('/auth')

