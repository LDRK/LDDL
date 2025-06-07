from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib import messages

# Vista para cerrar sesión
def logout_view(request):
    logout(request)
    messages.info(request, 'Has cerrado sesión correctamente.')
    return redirect('login')
#fin de la vista Logout