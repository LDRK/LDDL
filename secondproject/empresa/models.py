from django.db import models

# Create your models here.
class Empleado(models.Model):
    id = models.AutoField(primary_key=True)
    foto = models.ImageField(upload_to='empleados', verbose_name='Imagen', null=True, blank=True, default='empleados/empleado_deful.png') 
    nombre = models.CharField(max_length=50)
    apellidoPatern = models.CharField(max_length=50)
    apellidoMatern = models.CharField(max_length=50)
    correo = models.EmailField(max_length=50)
    departamento = models.CharField(max_length=50)
    
    
    
    def delete(self, using=None, keep_parents = False):
        self.foto.storage.delete(self.foto.name)
        super().delete()
