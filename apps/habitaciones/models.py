from django.db import models

class Habitacion(models.Model):
    TIPO_CHOICES = [
        ('simple', 'Simple'),
        ('doble', 'Doble'),
        ('matrimonial', 'Matrimonial'),
        ('suite', 'Suite'),
        ('triple', 'Triple'),
    ]

    ESTADO_CHOICES = [
        ('disponible', 'Disponible'),
        ('ocupada', 'Ocupada'),
        ('mantenimiento', 'Mantenimiento'),
    ]

    numero = models.CharField(max_length=10, unique=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    costo_diario = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='disponible')
    caracteristicas = models.TextField(blank=True)
    capacidad_personas = models.PositiveIntegerField(default=2) 

    def __str__(self):
        return f"Habitación {self.numero} ({self.get_tipo_display()})"

