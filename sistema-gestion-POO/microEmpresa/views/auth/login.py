from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from ...forms import CustomAuthenticationForm
from ...models.usuario import User 
from django.contrib import messages
from django.http import JsonResponse



#Creamos la vista de Login
def login_view(request):
    if request.user.is_authenticated:
        return redirect('admin')

    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data.get('username')  # Puede ser username o email
            password = form.cleaned_data.get('password')
            # print(f"Intentando autenticar con: {username_or_email}")

            # Intentar autenticar directamente con username
            user = authenticate(request, username=username_or_email, password=password)

            # Si no encuentra con username, buscamos por email
            if user is None:
                try:
                    user_obj = User.objects.get(email=username_or_email)
                    print(f"Usuario encontrado por email: {user_obj.username}")
                    user = authenticate(request, username=user_obj.username, password=password)
                except User.DoesNotExist:
                    print("No se encontró usuario con ese email.")
                    user = None

            if user is not None:
                login(request, user)
                return redirect_user_by_role(user)
            else:
                return render(request, 'login.html', {'error': 'Credenciales incorrectas'})
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'auth/login.html', {'form': form})

#Fin de la vista Login

#Funcion para redireccion al dashboard segun su rol
def redirect_user_by_role(user):
    """ Redirige al usuario al dashboard según su rol """
    if user.is_superuser == True:
        return redirect('admin')
    elif user.profile.role == "manager":
        return redirect('gerente')
    elif user.profile.role == "store":
        return redirect('inventario')
    elif user.profile.role == "sales":
        return redirect('ventas')
    else:
        return redirect('inicio')


