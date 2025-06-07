from django.contrib import admin
from .models import Empleado

# Register your models here.
# admin.site.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    # Especifica las columnas que quieres mostrar en la lista del admin
    list_display = ('id', 'nombre', 'apellidoPatern', 'apellidoMatern', 'correo', 'departamento')
    
    # Agrega filtros por campos específicos
    list_filter = ('departamento',)

    # Agrega una barra de búsqueda
    search_fields = ('nombre', 'apellidoPaterno', 'apellidoMaterno', 'correo')

    # Ordena la lista por un campo
    ordering = ('id',)

    # Muestra campos en detalle y formularios de edición
    fields = ( 'nombre', 'apellidoPaterno', 'apellidoMaterno', 'correo', 'departamento')


# Registra el modelo con la configuración personalizada
admin.site.register(Empleado, EmpleadoAdmin)