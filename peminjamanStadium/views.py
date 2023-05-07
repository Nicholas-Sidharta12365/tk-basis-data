from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'peminjaman_stadium.html')

def cek_sesi(request):
    return render(request, 'cek_sesi.html')

def pesan_stadium(request):
    return render(request, 'pesan_stadium.html')