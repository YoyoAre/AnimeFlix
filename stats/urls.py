from django.urls import path
from . import views

urlpatterns = [
    path('', views.p1, name='prueba'),
    path('p2', views.p2, name='prueba2'),
    
]