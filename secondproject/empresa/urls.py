from django.urls import path
from . import views
from django.conf import settings
from django.contrib.staticfiles.urls import static

urlpatterns = [
    path('', views.inicio, name='inicio'),
    #Rutas de acceso
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    #Rutas del dashboard del administrador
    path('dashboard/', views.dashboard, name='dashboard'),
    path('registroEmpleados/', views.registroEmpleados, name='registroEmpleados'),
    path('tablaEmpleados/', views.tablaEmpleados, name='tablaEmpleados'),
    path('dashboard/editar/<int:id>/', views.editarEmpleado, name='editarEmpleado' ),
    path('eliminar/<int:id>', views.deleteEmpleado, name='eliminar'),
    path('dashboard/usuarios/', views.usuarios, name='usuarios'),
    #Urls de los reportes de pdf
    path('dashboard/reportes/', views.reportes, name='reportes'),
    path('dashboard/reportes/pdf/', views.generar_pdf, name='generar_pdf'),
    #Urls para el manejo de excel
    path('cargar-excel/', views.cargar_excel, name='cargar_excel'),
    # path('tablaEmpleados/', views.ListaEmpleadosView.as_view(), name='tablaEmpleados'),
    #Rutas para el manejo de usuarios de la aplicacion
    path('tablaUsuarios/', views.tablaUsuarios, name='tablaUsuarios'),
    path('formUsuarios/', views.formUsuarios, name='formUsuarios'),
    path('registroUsuarios/', views.registroUsuarios, name='registroUsuarios'),
    path('usuarios/editar/<int:id>/', views.editarUsuario, name='editarUsuario'),
    path('usuarios/eliminar/<int:id>', views.deleteUser, name='eliminarUser'),

    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)