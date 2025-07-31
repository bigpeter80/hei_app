from apps.habitaciones.models import Habitacion
from apps.reservas.models import Reserva
from django.db.models import Q

def habitaciones_disponibles(fecha_entrada, fecha_salida):
    habitaciones_ocupadas = Reserva.objects.filter(
        eliminado=False,
        estado__in=['reservado', 'ocupado'],  # ignoramos las finalizadas
        fecha_entrada__lt=fecha_salida,
        fecha_salida__gt=fecha_entrada
    ).values_list('habitacion_id', flat=True)

    disponibles = Habitacion.objects.exclude(id__in=habitaciones_ocupadas)
    return disponibles
