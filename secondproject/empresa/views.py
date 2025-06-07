from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import pandas as pd
from .models import Empleado
from .forms import EmpleadoForm, RegistroForm, CustomAuthenticationForm, User
import json
from django.views.decorators.csrf import csrf_exempt 
from django.shortcuts import get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.db import transaction 
import os
import logging
from django.views.generic import ListView
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from datetime import datetime






# Create your views here.
def inicio(request):
    return render(request, 'pages/home.html')

# Vista para el registro
def register_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Inicia sesión automáticamente después del registro
            messages.success(request, 'Registro exitoso. ¡Bienvenido!')
            return redirect('login')  # Cambia a donde quieras redirigir después del registro
        else:
            messages.error(request, 'Por favor, corrige los errores.')
    else:
        form = RegistroForm()
    return render(request, 'auth/register.html', {'form': form})

# Vista para el login
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'¡Bienvenido {username}!')
                return redirect('dashboard')  # Cambia 'home' por la página principal de tu sitio
            else:
                messages.error(request, 'Usuario o contraseña incorrectos.')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'auth/login.html', {'form': form})


# Vista para cerrar sesión
def logout_view(request):
    logout(request)
    messages.info(request, 'Has cerrado sesión correctamente.')
    return redirect('login')




#Vistas de Dasboard
def dashboard(request):
    return render(request, 'dashboard/dashboard.html')

#Vista para registrar empleados.
@csrf_exempt  # Si no estás enviando el token CSRF con tu solicitud
def registroEmpleados(request):
    if request.method == 'POST':
        try:
            # Crear una instancia del formulario con los datos
            form = EmpleadoForm(request.POST, request.FILES)

            if form.is_valid():
                # Guardar los datos en la base de datos
                form.save()
                
                return JsonResponse({'ok': True, 'message': 'Empleado registrado exitosamente', 'redirect_url': '/dashboard/'})
            else:
                # Retornar los errores del formulario en formato JSON
                return JsonResponse({'ok': False, 'errors': form.errors}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'ok': False, 'message': 'Error al procesar los datos JSON'}, status=400)

    else:
        # Si no es un POST, renderizar el formulario
        return render(request, 'dashboard/formEmpleado.html')

#Tabla para mostrar los empleados
def tablaEmpleados(request):
    empleados = Empleado.objects.all() #Obtengo los empleados de la BD.
    return render(request, 'dashboard/tablaEmpleados.html', {'empleados': empleados})

def editarEmpleado(request, id):
    empleado = get_object_or_404(Empleado, id=id)
    form = EmpleadoForm(request.POST, request.FILES, instance=empleado)
    if form.is_valid() and request.method == 'POST':
        form.save()  # Guardar los cambios en el empleado
        return redirect('dashboard')  # Redirigir a la lista de empleados u otra página      
    
      # Si es una solicitud GET, cargar el formulario con los datos del empleado
        #form = EmpleadoForm(instance=empleado)
    
    # Renderizar el formulario
    return render(request, 'dashboard/formEmpleado.html', {'form': form,'empleado': empleado})


logger = logging.getLogger(__name__)            
@csrf_exempt
def cargar_excel(request):
    if request.method == 'POST' and request.FILES.get('archivo_excel'):
        archivo = request.FILES['archivo_excel']
        extension = os.path.splitext(archivo.name)[1]
        file_path = None

        # Validar si es un archivo Excel
        if extension.lower() not in ['.xlsx', '.xls']:
            messages.error(request, "Formato de archivo no válido. Solo se permiten .xlsx y .xls.")
            return redirect('registroEmpleados')

        try:
            # Guardar el archivo temporalmente
            fs = FileSystemStorage(location='media/')
            filename = fs.save(archivo.name, archivo)
            file_path = fs.path(filename)

            # Leer el archivo Excel con pandas
            df = pd.read_excel(file_path, engine='openpyxl')
            logger.info(f"Columnas encontradas en el Excel: {df.columns.tolist()}")

            # Normalizar nombres de columnas
            df.columns = df.columns.str.strip().str.lower()

            # Validar si tiene las columnas correctas
            columnas_requeridas = ['nombre', 'apellidopatern', 'apellidomatern', 'correo', 'departamento']
            columnas_faltantes = [col for col in columnas_requeridas if col not in df.columns]
            
            if columnas_faltantes:
                messages.error(request, f"Faltan las siguientes columnas: {', '.join(columnas_faltantes)}")
                return redirect('registroEmpleados')

            # Limpiar datos
            df = df.fillna('')  # Reemplazar NaN con string vacío
            
            # Validar datos antes de insertar
            errores = []
            for index, row in df.iterrows():
                if not row['nombre'].strip():
                    errores.append(f"Fila {index + 2}: El nombre es obligatorio")
                if not row['correo'].strip():
                    errores.append(f"Fila {index + 2}: El correo es obligatorio")
                # Agregar más validaciones según necesites

            if errores:
                messages.error(request, "Errores en el archivo Excel:\n" + "\n".join(errores))
                return redirect('registroEmpleados')

            # Insertar los datos en la base de datos usando una transacción
            with transaction.atomic():
                empleados_creados = 0
                for index, row in df.iterrows():
                    Empleado.objects.create(
                        nombre=row['nombre'].strip(),
                        apellidoPatern=row['apellidopatern'].strip(),
                        apellidoMatern=row['apellidomatern'].strip(),
                        correo=row['correo'].strip(),
                        departamento=row['departamento'].strip()
                    )
                    empleados_creados += 1

                messages.success(
                    request, 
                    f"Se han registrado correctamente {empleados_creados} empleados desde el Excel."
                )
                logger.info(f"Se crearon {empleados_creados} empleados exitosamente")

        except pd.errors.EmptyDataError:
            messages.error(request, "El archivo Excel está vacío.")
            logger.error("Se intentó procesar un archivo Excel vacío")
        
        except Exception as e:
            logger.error(f"Error al procesar el archivo Excel: {str(e)}", exc_info=True)
            messages.error(request, f"Error al procesar el archivo: {str(e)}")
            
        finally:
            # Limpiar archivo temporal
            if file_path and os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"Archivo temporal eliminado: {file_path}")

        return redirect('dashboard')

    return redirect('dashboard')

def deleteEmpleado(request, id):
    libro = Empleado.objects.get(id=id)
    libro.delete()
    return redirect('dashboard')

#Vista para el manejo de usuarios de la aplicacion
def usuarios(request):
    return render(request, 'dashboard/usuarios.html')

def tablaUsuarios(request):
    usuarios = User.objects.all()
    return render(request, 'dashboard/tablaUsuarios.html', {'usuarios': usuarios})

#Vista para registrar Usuarios.
@csrf_exempt  # Si no estás enviando el token CSRF con tu solicitud
def registroUsuarios(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        try:
            if form.is_valid():
                # Guardar los datos en la base de datos
                form.save()
                
                return JsonResponse({'ok': True, 'message': 'Usuario registrado exitosamente', 'redirect_url': '/dashboard/usuarios/'})
            else:
                # Retornar los errores del formulario en formato JSON
                return JsonResponse({'ok': False, 'errors': form.errors}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'ok': False, 'message': 'Error al procesar los datos JSON'}, status=400)

    else:
        # Si no es un POST, renderizar el formulario
        return render(request, 'dashboard/formUsuario.html',{'form': form})
    

def editarUsuario(request, id):
    usuario = get_object_or_404(User, id=id)
    form = RegistroForm(request.POST, instance=usuario)
    if form.is_valid() and request.method == 'POST':
        user = form.save(commit=False)
            
        # Si se ingresó una nueva contraseña, actualizarla
        password1 = form.cleaned_data.get("password1")
        password2 = form.cleaned_data.get("password2")
 
        if password1 and password2 and password1 == password2:
            user.set_password(password1)  # Encriptar contraseña
            
            user.save()
            return redirect('usuarios')    
    else:
        form = RegistroForm(instance=usuario)
    # Renderizar el formulario
    return render(request, 'dashboard/formUsuario.html', {'form': form,'usuario': usuario})

def deleteUser(request, id):
    usuario = User.objects.get(id=id)
    usuario.delete()
    return redirect('usuarios')

def formUsuarios(request):
    return render(request, 'dashboard/formUsuario.html')


def reportes(request):
    return render(request, 'dashboard/reportes.html')

def generar_pdf(request):
    tipo = request.GET.get('tipo', 'empleados')  # Obtener el parámetro 'tipo' (por defecto 'empleados')

    # Configurar la respuesta para mostrar el PDF en el navegador
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="reporte_{tipo}.pdf"'  # Mostrar en pestaña nueva

    # Crear el PDF
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    # Título dinámico
    if tipo == 'empleados':
        titulo = "Reporte de Empleados"
        headers = ["ID", "Nombre", "Apellido Paterno", "Apellido Materno", "Correo", "Departamento"]
        data = Empleado.objects.all()
    elif tipo == 'usuarios':
        titulo = "Reporte de Usuarios"
        headers = ["ID", "Nombre", "Correo", "Login"]
        data = User.objects.all()
    else:
        return HttpResponse("Tipo de reporte no válido", status=400)

    # Dibujar el título
    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, height - 50, titulo)

    # Coordenadas iniciales
    start_x = 50  # Margen izquierdo
    start_y = height - 100  # Posición inicial en Y

    # Ajustar anchos de columnas según el tipo de reporte
    if tipo == 'empleados':
        column_widths = [40, 70, 95, 95, 150, 80]
    else:  # Para usuarios
        column_widths = [40, 150, 200, 100]

    # Dibujar cabecera de la tabla
    p.setFont("Helvetica-Bold", 10)
    x_position = start_x
    for i, header in enumerate(headers):
        p.drawString(x_position, start_y, header)
        x_position += column_widths[i]

    # Línea separadora
    p.line(start_x, start_y - 5, start_x + sum(column_widths), start_y - 5)

    # Dibujar los datos en la tabla
    y = start_y - 25  # Posición inicial para los datos
    p.setFont("Helvetica", 10)
    
    for item in data:
        x_position = start_x
        if tipo == 'empleados':
            p.drawString(x_position, y, str(item.id))
            x_position += column_widths[0]
            p.drawString(x_position, y, item.nombre)
            x_position += column_widths[1]
            p.drawString(x_position, y, item.apellidoPatern)
            x_position += column_widths[2]
            p.drawString(x_position, y, item.apellidoMatern)
            x_position += column_widths[3]
            p.drawString(x_position, y, item.correo)
            x_position += column_widths[4]
            p.drawString(x_position, y, item.departamento)
        else:  # Para usuarios
            p.drawString(x_position, y, str(item.id))
            x_position += column_widths[0]
            p.drawString(x_position, y, item.username)
            x_position += column_widths[1]
            p.drawString(x_position, y, item.email)
            x_position += column_widths[2]
            if isinstance(item.last_login, datetime):
                p.drawString(x_position, y, item.last_login.strftime("%Y-%m-%d %H:%M:%S"))  # Formato deseado
            else:
                p.drawString(x_position, y, str(item.last_login))  # Si no es datetime, conviértelo a str

        y -= 20  # Espaciado entre filas

    # Guardar el PDF
    p.showPage()
    p.save()

    return response



# class ListaEmpleadosView(ListView):
#     model = Empleado
#     template_name = 'dashboard/tablaEmpleados.html'
#     context_object_name = 'empleados'
#     paginate_by = 5  # Número de empleados por página

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['is_paginated'] = self.get_paginate_by(self.queryset) is not None
#         return context