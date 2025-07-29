from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from apps.clientes.models import Cliente
from apps.habitaciones.models import Habitacion


class ReservaQuerySet(models.QuerySet):
    def activas(self):
        return self.filter(eliminado=False)


class ReservaManager(models.Manager):
    def get_queryset(self):
        return ReservaQuerySet(self.model, using=self._db).activas()


class Reserva(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    habitacion = models.ForeignKey(Habitacion, on_delete=models.PROTECT)
    fecha_entrada = models.DateField()
    fecha_salida = models.DateField()
    costo_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deposito = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    informacion_adicional = models.TextField(blank=True, null=True)

    # Auditoría
    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='reservas_creadas'
    )
    modificado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='reservas_modificadas'
    )
    creado_en = models.DateTimeField(auto_now_add=True)
    modificado_en = models.DateTimeField(auto_now=True)

    # Soft delete
    eliminado = models.BooleanField(default=False)

    # Managers
    objects = ReservaManager()  # Por defecto, solo reservas no eliminadas
    all_objects = models.Manager()  # Para acceder a todas las reservas, incluso eliminadas

    class Meta:
        indexes = [
            models.Index(fields=['cliente']),
            models.Index(fields=['habitacion']),
            models.Index(fields=['fecha_entrada']),
            models.Index(fields=['fecha_salida']),
        ]
        ordering = ['-fecha_entrada']

    def dias_reserva(self):
        dias = (self.fecha_salida - self.fecha_entrada).days
        return max(dias, 1)

    def calcular_costo_total(self):
        return self.dias_reserva() * self.habitacion.costo_diario

    def clean(self):
        if self.fecha_salida <= self.fecha_entrada:
            raise ValidationError("La fecha de salida debe ser posterior a la fecha de entrada.")

    def save(self, *args, **kwargs):
        self.full_clean()  # aplica las validaciones definidas en clean()
        if self.fecha_entrada and self.fecha_salida and self.habitacion:
            self.costo_total = self.calcular_costo_total()
        super().save(*args, **kwargs)

    @property
    def esta_activa(self):
        return not self.eliminado

    def __str__(self):
        return f"Reserva de {self.cliente} - Habitación {self.habitacion.numero}"
