from django.shortcuts import redirect, render
from django.conf import settings
import psycopg2

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
        adress = None
        role = None
        status = None
        rank = None

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
                adress = result_non_pemain[0][5]
                role = table

                if(role == 'panitia'):
                    rank = result[0][1]

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
            'role': role,
            'fname': fname,
            'lname': lname,
            'phone': phone,
            'email': email,
            'adress': adress,
            'status': status,
            'rank': rank
        }

    else:
        return redirect('/auth')

    return render(request, 'dashboard.html', context)