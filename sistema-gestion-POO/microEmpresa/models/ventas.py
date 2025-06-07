from django.db import models
from django.contrib.auth.models import User
from .cliente import Cliente
from .producto import Producto

class Venta(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=0, default=0)

    def obtener_detalles(self):
        return self.detalles.select_related('producto')

    def calcular_total(self):
        from django.db.models import Sum
        return self.detalles.aggregate(total=Sum('subtotal'))['total'] or 0

    
    def __str__(self):
        return f"Venta #{self.id} - {self.fecha.date()} - Cliente: {self.cliente}"
    

class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=0)
    subtotal = models.DecimalField(max_digits=10, decimal_places=0)

    def __str__(self):
        return f"{self.producto} x {self.cantidad}"
   