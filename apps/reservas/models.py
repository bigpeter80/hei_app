from django.db import models
from django.conf import settings
from apps.clientes.models import Cliente
from apps.habitaciones.models import Habitacion

class Reserva(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    habitacion = models.ForeignKey(Habitacion, on_delete=models.PROTECT)
    fecha_entrada = models.DateField()
    fecha_salida = models.DateField()
    costo_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deposito = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    informacion_adicional = models.TextField(blank=True, null=True)

    # Auditoría y control
    creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='reservas_creadas')
    modificado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='reservas_modificadas')
    creado_en = models.DateTimeField(auto_now_add=True)
    modificado_en = models.DateTimeField(auto_now=True)
    eliminado = models.BooleanField(default=False)

    def dias_reserva(self):
        dias = (self.fecha_salida - self.fecha_entrada).days
        return max(dias, 1)

    def calcular_costo_total(self):
        return self.dias_reserva() * self.habitacion.costo_diario

    def save(self, *args, **kwargs):
        if self.fecha_entrada and self.fecha_salida and self.habitacion:
            self.costo_total = self.calcular_costo_total()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Reserva de {self.cliente} - Habitación {self.habitacion.numero}"
