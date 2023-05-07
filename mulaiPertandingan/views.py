from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index_mulai_pertandingan.html')

def add_peristiwa(request):
    return render(request, 'add_peristiwa.html')