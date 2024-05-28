from django.db import models
from decimal import Decimal

class Productos(models.Model):
    producto_id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.IntegerField(default=1) 

    def __str__(self):
        return self.nombre

    @property
    def subtotal(self):
        return self.precio * self.cantidad
