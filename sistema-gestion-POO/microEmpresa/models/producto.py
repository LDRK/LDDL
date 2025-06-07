from django.db import models
from .categoria_producto import Categoria
from django.contrib.auth.models import User

class Producto(models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=12, decimal_places=0)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='productos')
    
    @classmethod
    def total_productos(cls):
        return cls.objects.count()
    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

    def __str__(self):
        return self.nombre


class MovimientoInventario(models.Model):
    TIPO_MOVIMIENTO = [
        ('registro', 'Registro'),
        ('actualizacion', 'Actualización'),
        ('eliminacion', 'Eliminación'),
        ('ajuste', 'Ajuste manual'),
    ]
    
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=TIPO_MOVIMIENTO)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return f"{self.tipo} - {self.producto.nombre} ({self.fecha.strftime('%Y-%m-%d %H:%M')})"
