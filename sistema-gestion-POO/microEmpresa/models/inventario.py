from django.db import models
from .producto import Producto

class Inventario(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='inventarios')
    cantidad = models.IntegerField()
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    #Consulta para trarl el stock de la base de datos
    @classmethod
    def total_stock(cls):
        return cls.objects.aggregate(total=models.Sum('cantidad'))['total'] or 0

    @classmethod
    def stock_bajo(cls, umbral=5):
        return cls.objects.filter(cantidad__lt=umbral).count()

    class Meta:
        verbose_name = 'Inventario'
        verbose_name_plural = 'Inventarios'

    def __str__(self):
        return f'{self.producto.nombre} - {self.cantidad} unidades'


