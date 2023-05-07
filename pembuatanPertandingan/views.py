from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index_create.html')

def add_pertandingan_index(request):
    return render(request, 'add_pertandingan_index.html')

def list_waktu(request):
    return render(request, 'waktu.html')

def create_pertandingan(request):
    return render(request, 'create_pertandingan.html')

