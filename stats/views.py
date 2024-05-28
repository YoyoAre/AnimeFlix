from django.shortcuts import render
from django.http import HttpResponse
def p1(request):
    return HttpResponse('¡Hola Mundo! :)')
def p2(request):
    try:
        mes = int(request.GET["mes"]) #si se hizo una busqueda por mes, el get da el numero del mes a buscar
    except:
        mes = 0 #sino, lo marca como 0
    try:
        año = int(request.GET["año"])#lo mismo para un año de busqueda
    except:
        año = 0
    print(request.GET)
    #print(Animes.objects.all())
    return HttpResponse(f"Año = {año}, mes = {mes}")