from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index_pembelian_tiket.html')

def list_waktu(request):
    return render(request, 'list_waktu.html')

def list_pertandingan(request):
    return render(request, 'list_pertandingan.html')

def beli_tiket(request):
    return render(request, 'beli_tiket.html')