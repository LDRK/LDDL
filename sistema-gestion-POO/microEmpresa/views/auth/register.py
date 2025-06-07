from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
#Creamos la vista de Register
def register(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Iniciar sesión después del registro
            return redirect('registerProfile')  # 
    else:
        form = RegistroForm()
    
    return render(request, 'auth/register.html', {'form': form})
#Fin de la vista Register