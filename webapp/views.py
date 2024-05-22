from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import *
import os
from django.core.paginator import Paginator
from django.conf import settings
from .forms import CambiarInformacionForm
from django.http import HttpResponse

User = get_user_model()

def webapp(request):
    messages.get_messages(request)  # Obtener mensajes almacenados
    all_animes = Animes.objects.all()
    paginator = Paginator(all_animes, 9)  # Mostrar 9 animes por página

    page_number = request.GET.get('page')
    animes = paginator.get_page(page_number)
    return render(request, 'webapp/index.html', {'animes': animes})


def anime_detail(request, nombre_anime):
    anime = get_object_or_404(Animes, nombre_anime=nombre_anime)
    episodios = Episodios.objects.filter(episodio_anime=anime)
    
    return render(request, 'webapp/anime_detail.html', {'anime': anime, 'episodios': episodios})

def reproductor(request, episodio_id):
    episodio = get_object_or_404(Episodios, id_episodio=episodio_id)
    
    return render(request, 'webapp/reproductor.html', {'episodio': episodio})

@login_required
def cuenta(request):
    user = request.user
    if request.method == 'POST':
        field_name = request.POST.get('field_name')
        new_value = request.POST.get('new_value')
        
        if field_name == 'username':
            user.username = new_value
        elif field_name == 'correo':
            user.email = new_value
        elif field_name == 'nombre':
            user.first_name = new_value
        elif field_name == 'apellido':
            user.last_name = new_value
        
        user.save()
        messages.success(request, 'La información de usuario ha sido actualizada exitosamente.')
        return redirect('cuenta')
    else:
        form = CambiarInformacionForm(instance=user)

    return render(request, 'webapp/cuenta.html', {'form': form})


@user_passes_test(lambda u: u.is_superuser)  # Verificar si el usuario es un administrador
@login_required  # Requiere que el usuario esté autenticado
def agregar_anime(request):
    animes = Animes.objects.all()
    if request.method == 'POST':
        id_anime = request.POST['id_anime']
        nombre_anime = request.POST['nombre_anime']
        descripcion_anime = request.POST['descripcion_anime']
        imagen_archivo = request.FILES['imagen_anime']
        portada_archivo = request.FILES['portada_anime']
        imagen_nombre = request.POST['nombre_imagen_anime']
        portada_nombre = request.POST['nombre_portada_anime']

        # Guardar las imágenes en tu directorio local
        imagen_path = os.path.join(settings.BASE_DIR, 'webapp', 'static', 'images', imagen_nombre)
        portada_path = os.path.join(settings.BASE_DIR, 'webapp', 'static', 'images', portada_nombre)

        with open(imagen_path, 'wb') as f:
            f.write(imagen_archivo.read())

        with open(portada_path, 'wb') as f:
            f.write(portada_archivo.read())

        # Crear el objeto Animes con los campos y nombres de imágenes
        anime = Animes(
            id_anime=id_anime,
            nombre_anime=nombre_anime,
            descripcion_anime=descripcion_anime,
            imagen_anime=os.path.join('images', imagen_nombre),
            portada_anime=os.path.join('images', portada_nombre)
        )
        anime.save()

    

    return render(request, 'webapp/agregar_anime.html', {'animes': animes})

@user_passes_test(lambda u: u.is_superuser)  # Verificar si el usuario es un administrador
@login_required  # Requiere que el usuario esté autenticado
def agregar_episodio(request):
    animes = Animes.objects.all()
    episodios = Episodios.objects.all()  # Valor predeterminado para la variable episodios

    if request.method == 'POST':
        # Obtener los datos del formulario
        id_episodio = request.POST['id_episodio']
        nombre_episodio = request.POST['nombre_episodio']
        nombre_episodio_extension = request.POST['extension']
        nombre_miniatura = request.POST['nombre_miniatura']
        temporada = request.POST['temporada']
        anime_id = request.POST['anime']
        imagen_anime = request.FILES['imagen_anime']
        episodio = request.FILES['episodio']
        anime = Animes.objects.get(id_anime=anime_id)

        # Guardar las imágenes en tu directorio local
        imagen_anime_path = os.path.join(settings.BASE_DIR, 'webapp', 'static', 'images', nombre_miniatura)
        imagen_episodio_path = os.path.join(settings.BASE_DIR, 'webapp', 'static', 'media', nombre_episodio_extension)

        with open(imagen_anime_path, 'wb') as f:
            f.write(imagen_anime.read())

        with open(imagen_episodio_path, 'wb') as f:
            f.write(episodio.read())

        # Crear el objeto Episodios y establecer la relación con el anime
        episodio = Episodios(
            id_episodio=id_episodio,
            nombre_episodio=nombre_episodio,
            temporada=temporada,
            ruta_imagen_episodio=os.path.join('images', nombre_miniatura),
            ruta_episodio=os.path.join('media', nombre_episodio_extension),
            episodio_anime=anime,
        )
        episodio.save()

        episodios = Episodios.objects.filter(episodio_anime=anime)
        return redirect('agregar_episodio')
    return render(request, 'webapp/agregar_episodios.html', {'animes': animes, 'episodios': episodios})




def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and check_password(password, user.password):
            login(request, user)
            messages.success(request, 'Inicio de sesión exitoso.')
            return redirect('webapp')  # Cambia 'webapp' con la URL de tu página principal
        else:
            messages.error(request, 'Credenciales inválidas. Inténtalo de nuevo.')
            return redirect('login')  # Cambia 'login' con la URL de tu página de inicio de sesión

    return render(request, 'webapp/login.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password1']
        nombre = request.POST['nombre']
        apellido = request.POST['apellido']
        email = request.POST['email']

        if Usuario.objects.filter(username=username).exists():
            messages.error(request, 'El usuario ya existe. Por favor, elige otro nombre de usuario.')
        else:
            # Realizar las acciones necesarias para registrar al usuario
            # Crea una instancia de Usuarios y guarda los datos
            user = Usuario(username=username, first_name=nombre, last_name=apellido, email=email)
            user.set_password(password)  # Establecer la contraseña utilizando set_password()
            user.save()
            messages.success(request, 'Registro exitoso. Inicia sesión con tu nueva cuenta.')
            return redirect('login')  # Cambia 'login' con la URL de tu página de inicio de sesión

    return render(request, 'webapp/register.html')

def logout_view(request):
    logout(request)
    return redirect('webapp')  # Cambia 'webapp' con la URL de tu página principal

import psycopg2

def con_psql(host = "192.168.1.128",db = "anime",query = "SELECT * FROM anime;"):
    #host = "192.168.1.128"
    #db = "anime"
    user = "azulito"
    pwd = "1234"
    conn = psycopg2.connect(
    host = host,dbname= db,
    user= user,password=pwd,port="5432"
    )
    cur = conn.cursor()

    #query = "SELECT * FROM anime;"
    print("Query: \n",query)
    cur.execute(query)

    try:
        res = cur.fetchall()
        print(res)
    except:
        res = []

    cur.close()
    conn.close()

    return res

import mariadb

def con_mariadb(query = "SELECT * FROM time;"):
    host = "192.168.1.145"
    db = "time"
    user = "azulito"
    pwd = "1234"
    conn = mariadb.connect(
    host = host,
    database= db,
    user= user,
    password= pwd,
    port=3306
    )
    cur = conn.cursor()

    cur.execute(query)

    try:
        res = cur.fetchall()
        print(res)
    except:
        res = []

    cur.close()
    conn.close()

    return res
import pandas as pd
import numpy as np

def stats(request):
    try:
        animes = con_psql("localhost","usuarios","""
        select * from dblink('dbname = anime hostaddr = 127.168.1.128
        user = azulito password = 1234',
        'select * from anime')
        as t1(id integer, nombre varchar);
        """)
    except:
        animes = []

    try:
        usuarios = con_psql("localhost","usuarios","select * from usuarios;")
    except:
        usuarios = []
    df1 = pd.DataFrame(np.empty(0, dtype=[('id', 'int'), ('Anime', 'str')]))
    df2 = pd.DataFrame(np.empty(0, dtype=[('id', 'int'), ('Time', 'str')]))
    df3 = pd.DataFrame(np.empty(0, dtype=[('id', 'int'), ('Usuario', 'str')]))
    

    Anime = "Animes: \n"
    i = 0
    for anime in animes:
        Anime = Anime + f"{str(anime[0])} - {anime[1]} \n"
        df1.loc[i] = anime
        i+=1
    df1 = df1.set_index("id")

    i=0
    for user in usuarios:
        #Anime = Anime + f"{str(anime[0])} - {anime[1]} \n"
        df3.loc[i] = user
        i+=1
    df3 = df3.set_index("id")

    i = 0
    try:
        times = con_mariadb()
    except:
        times = []
    Time = "Tiempo: \n"
    for time in times:
        Time = Time + f"{str(time[0])} - {time[1]}"
        df2.loc[i] = time
        i+=1

    df2 = df2.set_index('id')
    print(df1)
    print(df2)

    #result = pd.concat([df1, df2], axis=1,join="inner")
    result = pd.merge(df3,df1,how="left",left_index=True,right_index=True)
    result = pd.merge(result,df2,how="left",left_index=True,right_index=True)

    print(result)
    res = f"{Anime} \n {Time}"
    
    #return HttpResponse(res)
    return HttpResponse(result.to_html())

def estadistica(request):
