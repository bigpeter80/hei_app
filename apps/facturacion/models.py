# apps/facturacion/models.py
from django.db import models
from django.conf import settings
from apps.reservas.models import Reserva
from apps.consumos.models import Consumo

class Factura(models.Model):
    reserva = models.OneToOneField(Reserva, on_delete=models.PROTECT, related_name='factura')
    total_estadia = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_consumo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_general = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    creado_en = models.DateTimeField(auto_now_add=True)
    creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    eliminado = models.BooleanField(default=False)

    class Meta:
        ordering = ['-creado_en']

    def __str__(self):
        return f"Factura #{self.id} - Reserva #{self.reserva.id}"

class DetalleFactura(models.Model):
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE, related_name='detalles')
    descripcion = models.CharField(max_length=255)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ['factura', 'descripcion']

    def __str__(self):
        return f"{self.descripcion} x{self.cantidad}"
