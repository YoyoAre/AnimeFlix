from django.urls import path
from . import views

urlpatterns = [
    path('', views.webapp, name='webapp'),
    path('anime/<str:nombre_anime>/', views.anime_detail, name='anime_detail'),
    path('reproductor/<int:episodio_id>/', views.reproductor, name='reproductor'),
    path('agregar_anime/', views.agregar_anime, name='agregar_anime'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('cuenta/', views.cuenta, name='cuenta'),
    path('logout/', views.logout_view, name='logout'),
    path('accounts/login/', views.login_view, name='login'),
    path('agregar_episodio/', views.agregar_episodio, name= 'agregar_episodio'),
    path("estadistica/", views.estadistica, name="stats")

]