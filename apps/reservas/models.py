from django.db import models
from apps.clientes.models import Cliente
from apps.habitaciones.models import Habitacion

class Reserva(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    habitacion = models.ForeignKey(Habitacion, on_delete=models.CASCADE)
    fecha_entrada = models.DateField()
    fecha_salida = models.DateField()
    deposito = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    info_adicional = models.TextField(blank=True, null=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    def dias_reserva(self):
        return (self.fecha_salida - self.fecha_entrada).days

    def costo_total(self):
        return self.dias_reserva() * self.habitacion.costo_diario

    def __str__(self):
        return f"Reserva de {self.cliente} - Hab. {self.habitacion.numero}"
