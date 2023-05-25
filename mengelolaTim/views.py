from django.shortcuts import render, redirect
from utils.query import query

def index(request):
    
    user = request.session.get('logged_user')
    if (user== None):
        return redirect('/auth/login')
    if(user.get('role') != 'manajer'):
        if (user.get('role') == None):
            return redirect('/auth/login')
        return redirect(f'/dashboard/')
    id = query(f"""
        SELECT id_manajer from Manajer where username = '{user.get('username')}'
    """)[0]['id_manajer']

    if query(f''' SELECT nama_tim FROM TIM_MANAJER WHERE id_manajer = '{id}' ''') == []:
        # create message that says belum daftar tim
        context = {
            'pesan_error': 'Anda belum mendaftarkan tim'
        }
        return render(request, 'register_team.html', context)
    nama_tim = query(f''' SELECT nama_tim FROM TIM_MANAJER WHERE id_manajer = '{id}' ''')[0]['nama_tim']
    request.session['nama_tim'] = nama_tim
    pemain = query(f"""
        SELECT * from Pemain where nama_tim = '{nama_tim}'
        ORDER BY is_captain desc
    """)
    context = {
        'list_pemain': pemain,
        'login_status': 'hidden',
        'register_status': 'hidden',
        'manage_pertandingan_status': 'hidden',
        'pembelian_tiket_status': 'hidden',
        'rapat_status': 'hidden',
        'pembuatan_pertandingan_status': 'hidden',
        'mulai_pertandingan_status': 'hidden'
    }
    pelatih = query(f"""
        SELECT id, nama_depan, nama_belakang, nomor_hp,email, alamat, spesialisasi
        FROM NON_PEMAIN NP INNER JOIN SPESIALISASI_PELATIH SP on NP.id = SP.id_pelatih
        WHERE NP.id in (
        SELECT id_pelatih from pelatih
        where nama_tim = '{nama_tim}'
        )  
    """)
    context['list_pelatih'] = pelatih

    return render(request, 'mengelola.html', context)

def make_captain(request):
    id_pemain = request.POST['id']
    print(query(f''' UPDATE PEMAIN SET is_captain = true WHERE id_pemain = '{id_pemain}' '''))
    return redirect('/mengelola/')

def delete_pemain(request):
    id_pemain = request.POST.get('id')
    print(query(f''' UPDATE PEMAIN SET nama_tim = NULL WHERE id_pemain = '{id_pemain}' '''))
    
    return redirect('/mengelola/')

def delete_pelatih(request):
    id_pelatih = request.POST.get('id')
    print(query(f'''UPDATE PELATIH SET nama_tim = NULL WHERE id_pelatih = '{id_pelatih}' '''))
    return redirect('/mengelola/')

def register_team(request):
    user = request.session.get('logged_user')
    context = {
        'login_status': 'hidden',
        'register_status': 'hidden',
        'manage_pertandingan_status': 'hidden',
        'pembelian_tiket_status': 'hidden',
        'rapat_status': 'hidden',
        'pembuatan_pertandingan_status': 'hidden',
        'mulai_pertandingan_status': 'hidden'
    }
    if (request.method == 'POST'):
        nama_tim = request.POST.get('nama_tim')
        universitas = request.POST.get('universitas')
        print(nama_tim)
        print(universitas)

        response = query(f''' INSERT INTO TIM (nama_tim, universitas) VALUES ('{nama_tim}', '{universitas}') ''')
        if (isinstance(response, Exception)):
            context = {'message': "Nama tim sudah terdaftar"}
            return render(request, 'register_team.html', context)
        
        id = query(f'''
            SELECT id_manajer FROM MANAJER WHERE username = '{user.get('username')}'
            ''')[0]['id_manajer'] 
        response = query(f'''
            INSERT INTO TIM_MANAJER (id_manajer, nama_tim)
            VALUES ('{id}', '{nama_tim}')
            ''' )
        print(response)
        request.session['nama_tim'] = nama_tim
        return redirect('/mengelola/')

    return render(request, 'register_team.html')

def register_player(request):
    user = request.session.get('logged_user')
    if (user == None):
        return redirect('/auth/login')
    if(user.get('role') != 'manajer'):
        if (user.get('role') == None):
            return redirect('/auth/login')
        return redirect(f'/dashboard/')
    list_pemain = query(f''' SELECT * FROM PEMAIN WHERE nama_tim IS NULL ''')
    context = {'list_pemain': list_pemain,
        'login_status': 'hidden',
        'register_status': 'hidden',
        'manage_pertandingan_status': 'hidden',
        'pembelian_tiket_status': 'hidden',
        'rapat_status': 'hidden',
        'pembuatan_pertandingan_status': 'hidden',
        'mulai_pertandingan_status': 'hidden'
    }
    
    
    if (request.method == 'POST'):
        query(f''' UPDATE PEMAIN SET nama_tim = '{request.session.get('nama_tim')}' WHERE id_pemain = '{request.POST.get('pemain')}' ''')
        return redirect('/mengelola/')
    return render(request, 'register_player.html', context)

def register_trainer(request):
    user = request.session.get('logged_user')
    if (user == None):
        return redirect('/auth/login')
    if(user.get('role') != 'manajer'):
        if (user.get('role') == None):
            return redirect('/auth/login')
        return redirect(f'/dashboard/')
    list_pelatih = query(f''' SELECT p.id_pelatih, nama_depan, nama_belakang, string_agg(spesialisasi, ', ') as sp
    FROM non_pemain np
    JOIN pelatih p ON np.id = p.id_pelatih
    JOIN spesialisasi_pelatih sp ON p.id_pelatih = sp.id_pelatih
    WHERE p.nama_tim IS NULL
    GROUP BY p.id_pelatih, nama_depan, nama_belakang ''')

    context = {'list_pelatih': list_pelatih,
                'login_status': 'hidden',
                'register_status': 'hidden',
                'manage_pertandingan_status': 'hidden',
                'pembelian_tiket_status': 'hidden',
                'rapat_status': 'hidden',
                'pembuatan_pertandingan_status': 'hidden',
                'mulai_pertandingan_status': 'hidden'
    
    }
    if (request.method == 'POST'):
        print(request.POST.get('id'))
        response = query(f''' UPDATE PELATIH SET nama_tim = '{request.session.get('nama_tim')}' WHERE id_pelatih = '{request.POST.get('id')}' ''')
        if (isinstance(response, Exception)):
            context['message'] = response.args[0].split("\n")[0]
            return render(request, 'register_trainer.html', context)
        else: 
            return redirect('/mengelola/')
    return render(request, 'register_trainer.html', context)