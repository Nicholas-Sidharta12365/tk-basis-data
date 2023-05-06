# Tugas Kelompok Basis Data 2022 - 2023

## Kelompok
1. nama - npm 
2. Nicholas Sidharta - 2106752294
3. Vinsensius Ferdinando - 2106751221
4. nama - npm

# How to Run
1. Create venv
```
python -m venv env
```

2. Activate venv
```
Windows
env/Scripts/activate
Linux
source env/bin/activate
```

3. install dependencies
```
pip install -r requirements.txt
```

4. Run
```
python manage.py runserver
```

## Available Path
1. / = landing page
2. /auth = Choose Register or Login
3. /auth/register = register account page
4. /auth/login = login account page
5. /dashboard = dashboard page
6. /mengelola = mengelola tim
7. /mengelola/player = menambahkan player ke tabel player di mengelola tim
8. /mengelola/trainer = menambahkan pelatih ke tabel player di mengelola tim
9. /list = display list pertandingan
10. /history = display history rapat

N.B: Edit Navbar di /templates/base.html
