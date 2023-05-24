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

        # query_trigger = '''
        #                   CREATE OR REPLACE FUNCTION BUAT_PERTANDINGAN() RETURNS trigger AS
        #                   $$
        #                   BEGIN
        #                   
        #                   
        #                   
        #                   
        #                   
        #                   
        #                   
        #                   
        #                 '''
        query = '''
                    SELECT MIN(Nama_Tim) as TimA, MAX(Nama_Tim) as TimB
                    FROM sepak_bola.Tim_Pertandingan
                    GROUP BY ID_Pertandingan
                '''
        

        params = [user['username']]
        cur.execute(query, params)
        result = cur.fetchall() # Grup A

        # Query pembuatan trigger

        # buat_pertandingan_trigger = '''
        #             CREATE OR REPLACE FUNCTION BUAT_PERTANDINGAN() RETURNS trigger AS
        #             $$
        #             BEGIN
        #             IF (NEW.Stadium, NEW.Start_Datetime IN (
        #                 SELECT P.ID_Stadium, P.Start_Datetime
        #                 FROM sepak_bola.Peminjaman P
        #                 WHERE P.id_stadium = NEW.Stadium
        #                 AND (NEW.Start_datetime BETWEEN P.start_datetime AND P.end_datetime))
        #             )
        #             THEN
        #             RAISE EXCEPTION 'Stadium sedang dipinjam oleh %%', P.ID_Manajer;
        #             END IF;
        #             RETURN NEW;
        #             END;
        #             $$
        #             LANGUAGE plpgsql;

        #             CREATE TRIGGER BUAT_PERTANDINGAN
        #             BEFORE INSERT OR UPDATE ON sepak_bola.Pertandingan
        #             FOR EACH ROW EXECUTE PROCEDURE BUAT_PERTANDINGAN();
        # '''
        # cur.execute(buat_pertandingan_trigger, params)

        # tes_insert = '''
        # INSERT INTO sepak_bola.pertandingan (id_pertandingan, start_datetime, end_datetime, stadium)
        # values ('76d18b6c-964c-41ba-9099-3d79b16b3269', '2023-05-22 10:00:00', '2023-05-24 14:00:00', '26a755e2-18d6-4fbe-8923-d1a646e3e544');
        # '''
        # cur.execute(tes_insert, params)

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

