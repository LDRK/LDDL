from django.shortcuts import render
from .api import obtener_productos

def inicio(request):
    productos = obtener_productos() # LLamo la funcion donde consumo la api
    print(productos)
    return render(request, 'index.html', {'productos': productos})
