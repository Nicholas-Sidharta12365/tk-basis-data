from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'manage.html')

def peristiwa(request):
    return render(request, 'peristiwa.html')
