from django.db import models

class Cliente(models.Model):
    cedula = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo = models.EmailField()
    celular = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.cedula})"