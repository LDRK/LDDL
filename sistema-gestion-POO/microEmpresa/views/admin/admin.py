from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from ...models.usuario import Profile, User
from ...forms import ProfileForm,RegistroForm
@login_required
def superadmin_dashboard(request):
    return render(request, 'admin/admin_dashboard.html')

def register_users(request):
    if request.method == "POST":
        try:
            form = RegistroForm(request.POST)
            
            if form.is_valid():
                user = form.save()
                return JsonResponse({'ok': True, 'message': 'Usuario registrado exitosamente', 'user_id': user.id, 'redirect_url': '/registerProfile/'})
            
            else:
                # Retornar los errores del formulario en formato JSON
                return JsonResponse({'ok': False, 'errors': form.errors}, status=400)
            
        except json.JSONDecodeError:
            return JsonResponse({'ok': False, 'message': 'Error al procesar los datos JSON'}, status=400)
            
    else:
         # Si no es un POST, renderizar el formulario
        return render(request, 'admin/gestion_usuario/register_user.html')

def editar_users(request,user_id):
    usuario = get_object_or_404(User, id=user_id)

    if usuario.profile.role == "superadmin":
        messages.error(request, "No se puede editar el usuario superadmin.")
        return redirect('admin')  # Redirige a donde corresponda
    form = RegistroForm(request.POST,instance=usuario)
    if form.is_valid() and request.method == "POST":
        user = form.save(commit=False)
        
        # Si se ingresó una nueva contraseña, actualizarla
        password1 = form.cleaned_data.get("password1")
        password2 = form.cleaned_data.get("password2")
 
        if password1 and password2 and password1 == password2:
            user.set_password(password1)  # Encriptar contraseña
            
            user.save()
            #Guardamos el rol 
            role = form.cleaned_data.get('role')
            user.profile.role = role
            user.profile.save()
            return JsonResponse({'ok': True, 'redirect_url': '/dashboard/admin/users/'})  
        else:
            return JsonResponse({"ok": False, "errores": user.errors})
    else:
        form = RegistroForm(instance=usuario)
        return render(request, "admin/gestion_usuario/register_user.html", {"form": form,"usuario":usuario})

        
def editar_profile(request,user_id):
    usuario = get_object_or_404(User, id=user_id)
    
    perfil = get_object_or_404(Profile, user=usuario)
    
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=perfil)
        if form.is_valid():
            form.save()
            return JsonResponse({'ok': True, 'redirect_url': '/dashboard/admin/users/'})  
        else:
            return JsonResponse({"ok": False, "errores": form.errors})
    else:
        form = ProfileForm(instance=perfil)
        return render(request, "admin/gestion_usuario/register_profile.html", {
            "form": form,
            "usuario": usuario,
            "titulo": f"Editar perfil de {usuario.username}"
        })

#Creamos la vista para completar el perfil
def complete_profile(request):
    user_id = request.GET.get('user_id')  # Obtener el user_id desde la URL

    if request.method == 'POST':
        try:
            user_id = request.POST.get('user_id')  # Obtener user_id desde el formulario
            user = get_object_or_404(User, id=user_id)  # Buscar el usuario correcto
            profile, created = Profile.objects.get_or_create(user=user)
            form = ProfileForm(request.POST, instance=profile)
            if form.is_valid():
                form.save()
                return JsonResponse({'ok': True, 'redirect_url': '/dashboard/admin/users/'})  # Perfil guardado correctamente
            else:
                return JsonResponse({'ok': False, 'errors': form.errors})  # Errores en JSON
        
        except json.JSONDecodeError:
            return JsonResponse({'ok': False, 'message': 'Error al procesar los datos JSON'}, status=400)
            
    else:
        return render(request, 'admin/gestion_usuario/register_profile.html', {'form': ProfileForm(), 'user_id': user_id})
    
    
def mostrar_users(request):
    users = User.objects.all()  # Obtiene todos los usuarios
    user_profiles = Profile.objects.select_related('user')  # Une con la tabla de perfiles

    return render(request, "admin/gestion_usuario/mostrarUsers.html", {
        'users': users,
        'profiles': user_profiles
    })

def eliminar_usuario(request, user_id):
    usuario = get_object_or_404(User, id=user_id)
    
    if usuario.profile.role == "superadmin":
        messages.error(request, "No se puede eliminar al superadmin.")
        return redirect('admin')

    usuario.delete()
    messages.success(request, "Usuario eliminado correctamente.")
    return redirect('admin')