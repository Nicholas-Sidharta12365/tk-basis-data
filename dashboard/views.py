from django.shortcuts import redirect, render
from django.conf import settings
import psycopg2
import datetime

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
        tables = ['manajer', 'penonton', 'panitia']
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

        for table in tables:
            query = f"SELECT * FROM {schema_name}.{table} WHERE username = %s;"
            params = [user['username']]
            cur.execute(query, params)
            result = cur.fetchall()

            if result:
                query_non_pemain = f"SELECT * FROM {schema_name}.NON_PEMAIN WHERE id = %s;"
                params_non_pemain = [result[0][0]]
                cur.execute(query_non_pemain, params_non_pemain)
                result_non_pemain = cur.fetchall()

                fname = result_non_pemain[0][1]
                lname = result_non_pemain[0][2]
                phone = result_non_pemain[0][3]
                email = result_non_pemain[0][4]
                address = result_non_pemain[0][5]
                role = table
                
                if role == 'panitia':
                    rank = result[0][1]
                    query_rapat = f"SELECT * FROM {schema_name}.Rapat WHERE Datetime > %s AND Perwakilan_Panitia = %s ORDER BY Datetime;"
                    params_rapat = [current_datetime, result[0][0]]
                    cur.execute(query_rapat, params_rapat)
                    result_rapat = cur.fetchall()

                    upcoming_meetings = []
                    for rapat in result_rapat:
                        meeting_loop = {
                            'ID_Pertandingan': rapat[0],
                            'Datetime': rapat[1],
                            'Perwakilan_Panitia': rapat[2],
                            'Manajer_Tim_A': rapat[3],
                            'Manajer_Tim_B': rapat[4],
                            'Isi_Rapat': rapat[5]
                        }
                        upcoming_meetings.append(meeting_loop)

                    meeting = upcoming_meetings
                elif role == 'manajer':
                    query = f"SELECT tm.nama_tim, p.nama_depan, p.nama_belakang FROM {schema_name}.tim_manajer AS tm INNER JOIN {schema_name}.pemain AS p ON tm.Nama_Tim = p.nama_tim WHERE tm.ID_Manajer = %s;"
                    params_manajer = [result[0][0]]
                    cur.execute(query, params_manajer)
                    result_manajer = cur.fetchall()

                    team_player_list = []
                    for row in result_manajer:
                        team_name = row[0]
                        player_name = row[1] + " " + row[2]
                        team_found = False
                        for team_player in team_player_list:
                            if team_player["team_name"] == team_name:
                                team_player["player_names"].append(player_name)
                                team_found = True
                                break
                        if not team_found:
                            team_player_list.append({"team_name": team_name, "player_names": [player_name]})
                elif role == 'penonton':
                    query = f"SELECT p.ID_Pertandingan, p.Start_Datetime, p.End_Datetime, s.Nama FROM {schema_name}.Pembelian_Tiket AS pt INNER JOIN {schema_name}.Pertandingan AS p ON pt.id_pertandingan = p.ID_Pertandingan INNER JOIN {schema_name}.Stadium AS s ON p.Stadium = s.ID_Stadium WHERE pt.id_penonton = %s AND p.Start_Datetime > NOW();"
                    params_penonton = [result[0][0]] 
                    cur.execute(query, params_penonton)
                    result_pertandingan = cur.fetchall()

                    upcoming_pertandingan_list = []
                    for row in result_pertandingan:
                        pertandingan_id = row[0]
                        start_datetime = row[1]
                        end_datetime = row[2]
                        stadium_name = row[3]
                        upcoming_pertandingan_list.append({"pertandingan_id": pertandingan_id, "start_datetime": start_datetime, "end_datetime": end_datetime, "stadium_name": stadium_name})

                query_status = f"SELECT status FROM {schema_name}.status_non_pemain WHERE id_non_pemain = %s;"
                params_status = [result[0][0]]
                cur.execute(query_status, params_status)
                status_result = cur.fetchall()
                if status_result:
                    status = status_result[0][0]
                break

        cur.close()
        conn.close()

        context = {
            'fname': fname,
            'lname': lname,
            'phone': phone,
            'email': email,
            'address': address,
            'status': status,
            'rank': rank,
            'upcoming_meetings': meeting,
            'manajer_tim': team_player_list,
            'upcoming_pertandingan_list': upcoming_pertandingan_list
        }

        context.update(get_role_context(role))

        return render(request, 'dashboard.html', context)
    else:
        return redirect('/auth')
