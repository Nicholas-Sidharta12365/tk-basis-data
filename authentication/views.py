from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.http.response import JsonResponse
import json
from django.conf import settings
import psycopg2
import uuid

def index(request):

    if 'logged_user' not in request.session:
        context = {
            'navbar_status': 'hidden',
            'logout_status': 'hidden'
        }

        return render(request, 'auth.html', context)

    context = {}
    context.update(get_role_context(request.session.get('logged_user')['role']))
    
    return render(request, 'auth.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
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
        table_name = 'USER_SYSTEM'

        query = f"SELECT * FROM {schema_name}.{table_name} WHERE username = %s AND password = %s;"
        params = [username, password]

        cur.execute(query, params)

        result = cur.fetchone()

        if result:
            user = {
                'username': username,
                'password': password,
            }

            tables = ['manajer', 'penonton', 'panitia']
            for table in tables:
                query = f"SELECT * FROM {schema_name}.{table} WHERE username = %s;"
                params = [username]
                cur.execute(query, params)
                result = cur.fetchall()

                if result:
                    role = table
                    break
            else:
                role = None

            if role:
                user['role'] = role

            request.session['logged_user'] = user
            messages.success(request, 'Login successful!')
            cur.close()
            conn.close()
            return redirect('/dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
            cur.close()
            conn.close()
    else:
        if 'logged_user' not in request.session:
            context = {
                'navbar_status': 'hidden',
                'logout_status': 'hidden'
            }
            return render(request, 'login.html', context)

        context = {}
        context.update(get_role_context(request.session.get('logged_user')['role']))
        return render(request, 'login.html', context)

def register(request):
    if 'logged_user' not in request.session:
            context = {
                'navbar_status': 'hidden',
                'logout_status': 'hidden'
            }
            return render(request, 'register.html', context)

    context = {}
    context.update(get_role_context(request.session.get('logged_user')['role']))
    return render(request, 'register.html', context)

def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        db_config = settings.DATABASES['default']

        try:
            conn = psycopg2.connect(
                dbname=db_config['NAME'],
                user=db_config['USER'],
                password=db_config['PASSWORD'],
                host=db_config['HOST'],
                port=db_config['PORT']
            )

            cur = conn.cursor()

            schema_name = 'sepak_bola'
            table_name = 'USER_SYSTEM'

            query = f"INSERT INTO {schema_name}.{table_name} (username, password) VALUES (%s, %s)"
            params = [username, password]

            cur.execute(query, params)

            conn.commit()

            cur.close()
            conn.close()

            messages.success(request, 'Register successful!')
            return redirect("/auth/login")

        except psycopg2.Error as e:
            conn.rollback()

            print(f"An error occurred: {e}")
            messages.error(request, 'An error occurred during registration.')

        finally:
            if cur is not None:
                cur.close()
            if conn is not None:
                conn.close()

    else:
        if 'logged_user' not in request.session:
            context = {
                'navbar_status': 'hidden',
                'logout_status': 'hidden'
            }
            return render(request, 'user.html', context)

        context = {}
        context.update(get_role_context(request.session.get('logged_user')['role']))
        return render(request, 'user.html', context)

def register_panitia(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        nama_depan = request.POST.get('fname')
        nama_belakang = request.POST.get('lname')
        nomor_hp = request.POST.get('phone')
        email = request.POST.get('email')
        alamat = request.POST.get('address')
        status = request.POST.get('status')
        jabatan = request.POST.get('position')

        db_config = settings.DATABASES['default']

        try:
            conn = psycopg2.connect(
                dbname=db_config['NAME'],
                user=db_config['USER'],
                password=db_config['PASSWORD'],
                host=db_config['HOST'],
                port=db_config['PORT']
            )

            cur = conn.cursor()

            schema_name = 'sepak_bola'
            table_user = 'USER_SYSTEM'
            table_non_pemain = 'non_pemain'
            table_status = 'status_non_pemain'
            table_panitia = 'panitia'

            query_check = f"SELECT * FROM {schema_name}.{table_user} WHERE username = %s;"
            params_check = [username]

            cur.execute(query_check, params_check)

            result = cur.fetchone()

            if result:
                generated_uuid = uuid.uuid4()
                uuid_string = str(generated_uuid)

                query = f"INSERT INTO {schema_name}.{table_non_pemain} (ID, Nama_Depan, Nama_Belakang, Nomor_HP, Email, Alamat) VALUES (%s, %s, %s, %s, %s, %s)"
                params = [uuid_string, nama_depan, nama_belakang, nomor_hp, email, alamat]

                cur.execute(query, params)

                query_panitia = f"INSERT INTO {schema_name}.{table_panitia} (ID_Panitia, Jabatan, Username) VALUES (%s, %s, %s)"
                params_panitia = [uuid_string, jabatan, username]

                cur.execute(query_panitia, params_panitia)

                query_status = f"INSERT INTO {schema_name}.{table_status} (id_non_pemain, status) VALUES (%s, %s)"
                params_status = [uuid_string, status]

                cur.execute(query_status, params_status)

                conn.commit()

                cur.close()
                conn.close()

                messages.success(request, 'Register successful!')
                return redirect("/auth/login")
            else:
                cur.close()
                conn.close()
                messages.error("Username not found, please try again")

        except psycopg2.Error as e:
            conn.rollback()

            print(f"An error occurred: {e}")
            messages.error(request, 'An error occurred during registration.')

        finally:
            if cur is not None:
                cur.close()
            if conn is not None:
                conn.close()

    else:
        if 'logged_user' not in request.session:
            context = {
                'navbar_status': 'hidden',
                'logout_status': 'hidden'
            }
            return render(request, 'panitia.html', context)

        context = {}
        context.update(get_role_context(request.session.get('logged_user')['role']))
        return render(request, 'panitia.html', context)


def register_manajer(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        nama_depan = request.POST.get('fname')
        nama_belakang = request.POST.get('lname')
        nomor_hp = request.POST.get('phone')
        email = request.POST.get('email')
        alamat = request.POST.get('address')
        status = request.POST.get('status')

        db_config = settings.DATABASES['default']

        try:
            conn = psycopg2.connect(
                dbname=db_config['NAME'],
                user=db_config['USER'],
                password=db_config['PASSWORD'],
                host=db_config['HOST'],
                port=db_config['PORT']
            )

            cur = conn.cursor()

            schema_name = 'sepak_bola'
            table_user = 'USER_SYSTEM'
            table_non_pemain = 'non_pemain'
            table_status = 'status_non_pemain'
            table_manajer = 'Manajer'

            query_check = f"SELECT * FROM {schema_name}.{table_user} WHERE username = %s;"
            params_check = [username]

            cur.execute(query_check, params_check)

            result = cur.fetchone()

            if result:
                generated_uuid = uuid.uuid4()
                uuid_string = str(generated_uuid)

                query = f"INSERT INTO {schema_name}.{table_non_pemain} (ID, Nama_Depan, Nama_Belakang, Nomor_HP, Email, Alamat) VALUES (%s, %s, %s, %s, %s, %s)"
                params = [uuid_string, nama_depan, nama_belakang, nomor_hp, email, alamat]

                cur.execute(query, params)

                query_manajer = f"INSERT INTO {schema_name}.{table_manajer} (ID_Manajer, Username) VALUES (%s, %s)"
                params_manajer = [uuid_string, username]

                cur.execute(query_manajer, params_manajer)

                query_status = f"INSERT INTO {schema_name}.{table_status} (id_non_pemain, status) VALUES (%s, %s)"
                params_status = [uuid_string, status]

                cur.execute(query_status, params_status)

                conn.commit()

                cur.close()
                conn.close()

                messages.success(request, 'Register successful!')
                return redirect("/auth/login")
            else:
                cur.close()
                conn.close()
                messages.error("Username not found, please try again")

        except psycopg2.Error as e:
            conn.rollback()

            print(f"An error occurred: {e}")
            messages.error(request, 'An error occurred during registration.')

        finally:
            if cur is not None:
                cur.close()
            if conn is not None:
                conn.close()

    else:
        if 'logged_user' not in request.session:
            context = {
                'navbar_status': 'hidden',
                'logout_status': 'hidden'
            }
            return render(request, 'manajer.html', context)

        context = {}
        context.update(get_role_context(request.session.get('logged_user')['role']))
        return render(request, 'manajer.html', context)

def register_penonton(request):
        if request.method == 'POST':
            username = request.POST.get('username')
            nama_depan = request.POST.get('fname')
            nama_belakang = request.POST.get('lname')
            nomor_hp = request.POST.get('phone')
            email = request.POST.get('email')
            alamat = request.POST.get('address')
            status = request.POST.get('status')

            db_config = settings.DATABASES['default']

            try:
                conn = psycopg2.connect(
                    dbname=db_config['NAME'],
                    user=db_config['USER'],
                    password=db_config['PASSWORD'],
                    host=db_config['HOST'],
                    port=db_config['PORT']
                )

                cur = conn.cursor()

                schema_name = 'sepak_bola'
                table_user = 'USER_SYSTEM'
                table_non_pemain = 'non_pemain'
                table_status = 'status_non_pemain'
                table_manajer = 'Penonton'

                query_check = f"SELECT * FROM {schema_name}.{table_user} WHERE username = %s;"
                params_check = [username]

                cur.execute(query_check, params_check)

                result = cur.fetchone()

                if result:
                    generated_uuid = uuid.uuid4()
                    uuid_string = str(generated_uuid)

                    query = f"INSERT INTO {schema_name}.{table_non_pemain} (ID, Nama_Depan, Nama_Belakang, Nomor_HP, Email, Alamat) VALUES (%s, %s, %s, %s, %s, %s)"
                    params = [uuid_string, nama_depan, nama_belakang, nomor_hp, email, alamat]

                    cur.execute(query, params)

                    query_penonton = f"INSERT INTO {schema_name}.{table_manajer} (ID_Penonton, Username) VALUES (%s, %s)"
                    params_penonton = [uuid_string, username]

                    cur.execute(query_penonton, params_penonton)

                    query_status = f"INSERT INTO {schema_name}.{table_status} (id_non_pemain, status) VALUES (%s, %s)"
                    params_status = [uuid_string, status]

                    cur.execute(query_status, params_status)

                    conn.commit()

                    cur.close()
                    conn.close()

                    messages.success(request, 'Register successful!')
                    return redirect("/auth/login")
                else:
                    cur.close()
                    conn.close()
                    messages.error("Username not found, please try again")

            except psycopg2.Error as e:
                conn.rollback()

                print(f"An error occurred: {e}")
                messages.error(request, 'An error occurred during registration.')

            finally:
                if cur is not None:
                    cur.close()
                if conn is not None:
                    conn.close()

        else:
            if 'logged_user' not in request.session:
                context = {
                    'navbar_status': 'hidden',
                    'logout_status': 'hidden'
                }
                return render(request, 'penonton.html', context)

            context = {}
            context.update(get_role_context(request.session.get('logged_user')['role']))
            return render(request, 'penonton.html', context)

def logout(request):
    if 'logged_user' in request.session:
        del request.session['logged_user']
    return redirect('/auth')

def get_role_context(role):
    context = {
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