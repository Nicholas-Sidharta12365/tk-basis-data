"""sepakbola URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('landing.urls')),
    path('auth/', include('authentication.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('mengelola/', include('mengelolaTim.urls')),
    path('history/', include(('historyRapat.urls'))),
    path('list/', include(('listPertandingan.urls'))),
    path('pinjam/', include('peminjamanStadium.urls')),
    path('pembelian/', include('pembelianTiket.urls')),
    path('manage/', include('managePertandingan.urls')),
    path('creation/', include('pembuatanPertandingan.urls')),
    path('start/', include('mulaiPertandingan.urls')),
    path('rapat/', include('mulaiRapat.urls')),
]
