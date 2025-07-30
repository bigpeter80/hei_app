from django.db import transaction
from decimal import Decimal
from apps.facturacion.models import Factura, DetalleFactura
from apps.reservas.models import Reserva
from apps.consumos.models import Consumo
#from apps.restaurante.models import Consumo 

@transaction.atomic
def generar_factura(reserva: Reserva, usuario):
    total_estadia = reserva.costo_total
    consumos = reserva.consumos.all()
    total_consumos = sum([c.subtotal() for c in consumos])
    total_general = total_estadia + total_consumos

    # Crear factura principal
    factura = Factura.objects.create(
        reserva=reserva,
        total_estadia=total_estadia,
        total_consumo=total_consumos,
        total_general=total_general,
        creado_por=usuario
    )

    # Registrar detalle de cada consumo
    for consumo in consumos:
        DetalleFactura.objects.create(
            factura=factura,
            descripcion=consumo.descripcion,
            cantidad=consumo.cantidad,
            precio_unitario=consumo.precio_unitario,
            subtotal=consumo.subtotal()
        )

    return factura
