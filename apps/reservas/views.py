#reservas/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q
from django.template.loader import get_template
from xhtml2pdf import pisa
from datetime import datetime
from apps.habitaciones.models import Habitacion
from apps.clientes.models import Cliente
from .models import Reserva
from .forms import ReservaForm
from apps.facturacion.utils import generar_factura 
from apps.huespedes.models import Huesped
from django.views.decorators.http import require_POST
from django.db import transaction
from apps.habitaciones.utils import habitaciones_disponibles

# Crear una nueva reserva
@login_required
@transaction.atomic
def crear_reserva(request):
    if request.method == 'POST':
        fecha_entrada = request.POST.get('fecha_entrada')
        fecha_salida = request.POST.get('fecha_salida')

        form = ReservaForm(request.POST, fecha_entrada=fecha_entrada, fecha_salida=fecha_salida)

        if form.is_valid():
            reserva = form.save(commit=False)
            cliente_id = request.POST.get('cliente')
            try:
                reserva.cliente = Cliente.objects.get(id=cliente_id, eliminado=False)
            except Cliente.DoesNotExist:
                messages.error(request, 'El cliente seleccionado no existe.')
                return render(request, 'reservas/form.html', {'form': form})
    
        reserva.creado_por = request.user
        reserva.modificado_por = request.user
        reserva.save()
        form.save_m2m()
        messages.success(request, "Reserva registrada exitosamente.")
        return redirect('reservas:listado_reservas')
    else:
        form = ReservaForm()
    return render(request, 'reservas/form.html', {'form': form})

# Editar una reserva
@login_required
def editar_reserva(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk, eliminado=False)
    if request.method == 'POST':
        form = ReservaForm(request.POST, instance=reserva)
        if form.is_valid():
            reserva = form.save(commit=False)
            cliente_id = request.POST.get('cliente')
            if cliente_id:
                try:
                    reserva.cliente = Cliente.objects.get(id=cliente_id, eliminado=False)
                except Cliente.DoesNotExist:
                    messages.error(request, 'El cliente seleccionado no existe.')
                    return render(request, 'reservas/form.html', {'form': form, 'accion': 'Editar'})
            reserva.modificado_por = request.user
            reserva.save()
            messages.success(request, 'Reserva actualizada correctamente.')
            return redirect('reservas:detalle', pk=reserva.pk)
        messages.error(request, 'Corrige los errores del formulario.')
    else:
        form = ReservaForm(instance=reserva)
    return render(request, 'reservas/form.html', {'form': form, 'accion': 'Editar', 'reserva': reserva})

# Eliminar reserva (soft delete)
@login_required
def eliminar_reserva(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk, eliminado=False)
    reserva.eliminado = True
    reserva.modificado_por = request.user
    reserva.save()
    messages.success(request, 'Reserva cancelada correctamente.')
    return redirect('reservas:listado_reservas')

# Vista de detalle
@login_required
def reserva_detalle(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)
    return render(request, 'reservas/detalle.html', {'reserva': reserva})

# Exportar a PDF
@login_required
def reserva_exportar_pdf(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk, eliminado=False)
    template_path = 'reservas/pdf.html'
    context = {'reserva': reserva}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="reserva_{pk}.pdf"'
    html = get_template(template_path).render(context)
    pisa.CreatePDF(html, dest=response)
    return response

# Imprimir reserva (vista HTML)
@login_required
def reserva_imprimir(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk, eliminado=False)
    return render(request, 'reservas/pdf.html', {'reserva': reserva, 'imprimir': True})

# Listado con filtros
@login_required
def reserva_lista(request):
    reservas = Reserva.objects.select_related('cliente', 'habitacion').filter(eliminado=False).order_by('-creado_en')
    cliente_query = request.GET.get('cliente', '').strip()
    if cliente_query:
        reservas = reservas.filter(
            Q(cliente__nombre__icontains=cliente_query) |
            Q(cliente__apellido__icontains=cliente_query) |
            Q(cliente__dni__icontains=cliente_query)
        )
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    if fecha_inicio:
        reservas = reservas.filter(fecha_entrada__gte=fecha_inicio)
    if fecha_fin:
        reservas = reservas.filter(fecha_salida__lte=fecha_fin)

    paginator = Paginator(reservas, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'reservas/lista.html', {
        'page_obj': page_obj,
        'reservas': page_obj.object_list,
        'cliente_query': cliente_query,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
    })

# AJAX: Buscar cliente
@require_GET
@login_required
def buscar_cliente(request):
    term = request.GET.get('term', '')
    clientes = Cliente.objects.filter(
        Q(nombre__icontains=term) | Q(apellido__icontains=term) | Q(dni__icontains=term),
        eliminado=False
    )[:10]
    resultados = [{
        'id': c.id,
        'label': f'{c.nombre} {c.apellido} - {c.dni}',
        'value': f'{c.nombre} {c.apellido}',
        'dni': c.dni,
        'telefono': c.telefono,
        'email': c.email,
    } for c in clientes]
    return JsonResponse(resultados, safe=False)

@require_POST
@login_required
def crear_huesped_ajax(request):
    data = request.POST
    try:
        nuevo = Huesped.objects.create(
            nombre=data.get('nombre'),
            apellido=data.get('apellido'),
            dni=data.get('dni'),
            fecha_nacimiento=data.get('fecha_nacimiento'),
            direccion=data.get('direccion'),
            telefono=data.get('telefono'),
            creado_por=request.user,
            modificado_por=request.user
        )
        return JsonResponse({
            'success': True,
            'id': nuevo.id,
            'text': f"{nuevo.nombre} {nuevo.apellido} ({nuevo.dni})"
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
def buscar_huesped(request):
    term = request.GET.get('term', '')
    huespedes = Huesped.objects.filter(
        eliminado=False,
        dni__icontains=term
    ) | Huesped.objects.filter(
        eliminado=False,
        nombre__icontains=term
    ) | Huesped.objects.filter(
        eliminado=False,
        apellido__icontains=term
    )

    data = [
        {'id': h.id, 'nombre': h.nombre, 'apellido': h.apellido, 'dni': h.dni}
        for h in huespedes.distinct()[:10]
    ]
    return JsonResponse(data, safe=False)

# AJAX: Habitaciones disponibles
@require_GET
@login_required
def habitaciones_disponibles(request):
    entrada = request.GET.get('entrada')
    salida = request.GET.get('salida')
    disponibles = []

    if entrada and salida:
        try:
            entrada_dt = datetime.strptime(entrada, '%Y-%m-%d').date()
            salida_dt = datetime.strptime(salida, '%Y-%m-%d').date()
            if entrada_dt >= salida_dt:
                return JsonResponse([], safe=False)

            ocupadas = Reserva.objects.filter(
                eliminado=False,
                fecha_entrada__lt=salida_dt,
                fecha_salida__gt=entrada_dt
            ).values_list('habitacion_id', flat=True)

            disponibles = Habitacion.objects.exclude(id__in=ocupadas).values(
                'id', 'numero', 'tipo', 'estado', 'costo_diario'
            )
        except ValueError:
            return JsonResponse([], safe=False)

    return JsonResponse(list(disponibles), safe=False)

def obtener_habitaciones_disponibles(request):
    fecha_entrada = request.GET.get('fecha_entrada')
    fecha_salida = request.GET.get('fecha_salida')

    if fecha_entrada and fecha_salida:
        disponibles = habitaciones_disponibles(fecha_entrada, fecha_salida)
        data = [
            {
                'id': hab.id,
                'texto': f"{hab.numero} - {hab.tipo} (Gs. {hab.costo_diario})"
            } for hab in disponibles
        ]
        return JsonResponse({'habitaciones': data})
    return JsonResponse({'habitaciones': []})

@login_required
def reservas_eliminadas(request):
    cliente_query = request.GET.get('cliente', '')
    fecha_inicio = request.GET.get('fecha_inicio', '')
    fecha_fin = request.GET.get('fecha_fin', '')

    reservas = Reserva.objects.filter(eliminado=True)

    if cliente_query:
        reservas = reservas.filter(
            Q(cliente__nombre__icontains=cliente_query) |
            Q(cliente__apellido__icontains=cliente_query) |
            Q(cliente__dni__icontains=cliente_query)
        )

    if fecha_inicio:
        reservas = reservas.filter(fecha_entrada__gte=fecha_inicio)

    if fecha_fin:
        reservas = reservas.filter(fecha_salida__lte=fecha_fin)

    reservas = reservas.order_by('-fecha_entrada')
    paginator = Paginator(reservas, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'reservas/eliminadas.html', {
        'reservas': page_obj,
        'page_obj': page_obj,
        'cliente_query': cliente_query,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
    })

@login_required
@transaction.atomic
def checkin(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk, eliminado=False)

    if reserva.estado != 'reservado':
        messages.warning(request, 'La reserva debe estar en estado "reservado" para realizar el check-in.')
        return redirect('reservas:detalle', pk=pk)

    if request.method == 'POST':
        adultos = int(request.POST.get('adultos', 1))
        ninos = int(request.POST.get('ninos', 0))
        huespedes_ids = request.POST.getlist('huespedes')

        reserva.adultos = adultos
        reserva.ninos = ninos
        reserva.estado = 'ocupado'
        reserva.habitacion.estado = 'ocupada'
        reserva.modificado_por = request.user
        reserva.save()
        reserva.habitacion.save()

        # Asociar huéspedes seleccionados
        reserva.huespedes.clear()
        for h_id in huespedes_ids:
            try:
                huesped = Huesped.objects.get(pk=h_id, eliminado=False)
                reserva.huespedes.add(huesped)
            except Huesped.DoesNotExist:
                continue

        messages.success(request, 'Check-in realizado correctamente.')
        return redirect('reservas:detalle', pk=reserva.pk)

    else:
        # Prellenar adultos y niños desde la reserva (si existieran)
        adultos = reserva.adultos or 1
        ninos = reserva.ninos or 0

        # Cargar cliente como huésped si no está en la lista aún
        if not reserva.huespedes.filter(dni=reserva.cliente.dni).exists():
            huesped, creado = Huesped.objects.get_or_create(
                dni=reserva.cliente.dni,
                defaults={
                    'nombre': reserva.cliente.nombre,
                    'apellido': reserva.cliente.apellido,
                    'telefono': reserva.cliente.telefono,
                    'direccion': '',
                    'fecha_nacimiento': None,
                    'creado_por': request.user,
                    'modificado_por': request.user
                }
            )
            reserva.huespedes.add(huesped)

        return render(request, 'reservas/checkin.html', {
            'reserva': reserva,
            'huespedes': reserva.huespedes.all(),
            'adultos': adultos,
            'ninos': ninos,
        })


@login_required
def checkout(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk, eliminado=False)

    if reserva.estado != 'ocupado':
        messages.error(request, 'Solo las reservas en estado "ocupado" pueden finalizarse.')
        return redirect('reservas:listado_reservas')

    reserva.estado = 'finalizado'
    reserva.modificado_por = request.user
    reserva.save()

    generar_factura(reserva, request.user)  # Generación automática de factura

    messages.success(request, 'Check-out realizado. Reserva finalizada y factura generada.')
    return redirect('reservas:detalle', pk=reserva.pk)