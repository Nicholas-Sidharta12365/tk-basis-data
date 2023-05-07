from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index_rapat.html')

def pengisian_rapat(request):
    return render(request, 'pengisian_rapat.html')