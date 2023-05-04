from django.shortcuts import render

def index(request):

    return render(request, 'mengelola.html')

def register_team(request):

    return render(request, 'register_team.html')

def register_player(request):

    return render(request, 'register_player.html')

def register_trainer(request):

    return render(request, 'register_trainer.html')