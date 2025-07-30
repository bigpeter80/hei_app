from django.db import models
from apps.reservas.models import Reserva
from django.conf import settings

class Consumo(models.Model):
    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE, related_name='consumos')
    descripcion = models.CharField(max_length=255)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    creado_en = models.DateTimeField(auto_now_add=True)
    creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ['-creado_en']

    def subtotal(self):
        return self.cantidad * self.precio_unitario

    def __str__(self):
        return f"{self.descripcion} x{self.cantidad} - Reserva #{self.reserva.id}"


