# apps/reservas/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.timezone import now
from django.http import JsonResponse
from django.core.paginator import Paginator
from apps.habitaciones.models import Habitacion
from apps.clientes.models import Cliente
from .models import Reserva
from .forms import ReservaForm
from django.db.models import Q
from datetime import datetime

@login_required
def crear_reserva(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)

            # Obtener cliente desde el campo oculto
            cliente_id = request.POST.get('cliente')
            if cliente_id:
                try:
                    cliente = Cliente.objects.get(id=cliente_id, eliminado=False)
                    reserva.cliente = cliente
                except Cliente.DoesNotExist:
                    messages.error(request, 'El cliente seleccionado no existe.')
                    return render(request, 'reservas/form.html', {'form': form, 'accion': 'Nueva'})

            reserva.creado_por = request.user
            reserva.modificado_por = request.user
            reserva.save()
            messages.success(request, 'Reserva guardada correctamente.')
            return redirect('reservas:listado_reservas')
        else:
            messages.error(request, 'Corrige los errores del formulario.')
    else:
        form = ReservaForm()
    return render(request, 'reservas/form.html', {'form': form, 'accion': 'Nueva'})


@require_GET
@login_required
def buscar_cliente(request):
    term = request.GET.get('term', '')
    clientes = Cliente.objects.filter(nombre__icontains=term, eliminado=False)[:10]
    resultados = [
        {
            'id': cliente.id,
            'label': f'{cliente.nombre} {cliente.apellido} - {cliente.dni}',
            'value': f'{cliente.nombre} {cliente.apellido}',
            'dni': cliente.dni,
            'telefono': cliente.telefono,
            'email': cliente.email,
        }
        for cliente in clientes
    ]
    return JsonResponse(resultados, safe=False)

@login_required
def habitaciones_disponibles(request):
    entrada = request.GET.get('entrada')
    salida = request.GET.get('salida')
    disponibles = []

    if entrada and salida:
        reservas_superpuestas = Reserva.objects.filter(
            eliminado=False,
            fecha_entrada__lt=salida,
            fecha_salida__gt=entrada
        ).values_list('habitacion_id', flat=True)

        # Agrega 'costo_diario' al values()
        disponibles = Habitacion.objects.exclude(id__in=reservas_superpuestas).values(
        'id', 'numero', 'tipo', 'estado', 'costo_diario'
    )

    return JsonResponse(list(disponibles), safe=False)

from django.db.models import Q
from datetime import datetime

@login_required
def reserva_lista(request):
    reservas = Reserva.objects.select_related('cliente', 'habitacion').all().order_by('-creado_en')

    # Filtro por cliente (nombre, apellido o DNI)
    cliente_query = request.GET.get('cliente', '').strip()
    if cliente_query:
        reservas = reservas.filter(
            Q(cliente__nombre__icontains=cliente_query) |
            Q(cliente__apellido__icontains=cliente_query) |
            Q(cliente__dni__icontains=cliente_query)
        )

    # Filtro por fechas
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    if fecha_inicio:
        reservas = reservas.filter(fecha_entrada__gte=fecha_inicio)
    if fecha_fin:
        reservas = reservas.filter(fecha_salida__lte=fecha_fin)

    paginator = Paginator(reservas, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'reservas': page_obj.object_list,
        'cliente_query': cliente_query,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
    }
    return render(request, 'reservas/lista.html', context)
