from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.template.loader import render_to_string
from django.http import JsonResponse
from .models import Cliente
from .forms import ClienteForm

#obtiene el listado de clientes
@login_required
def cliente_lista(request):
    query = request.GET.get('q')
    clientes = Cliente.objects.all()

    if query:
        clientes = clientes.filter(
            Q(dni__icontains=query) |
            Q(nombre__icontains=query) |
            Q(apellido__icontains=query) |
            Q(email__icontains=query)
        )

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('clientes/tabla.html', {'clientes': clientes})
        return JsonResponse({'html': html})

    return render(request, 'clientes/lista.html', {'clientes': clientes, 'query': query})

# vista para creacion de nuevo cliente
@login_required
def cliente_create(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save(commit=False)
            cliente.modificado_por = request.user
            cliente.save()
            messages.success(request, 'Cliente creado exitosamente.')
            return redirect('clientes:listado_clientes')
        else:
            messages.error(request, 'Error al crear el cliente. Verifica los datos.')
    else:
        form = ClienteForm()
    return render(request, 'clientes/form.html', {'form': form, 'accion': 'Crear'})

#vista para actualización de datos de clientes
@login_required
def cliente_update(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            cliente = form.save(commit=False)
            cliente.modificado_por = request.user
            cliente.save()
            messages.success(request, 'Cliente actualizado correctamente.')
            return redirect('clientes:listado_clientes')
        else:
            messages.error(request, 'Error al actualizar el cliente.')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'clientes/form.html', {'form': form, 'accion': 'Editar'})

#vista para eliminacion de datos de clientes soft_delete
@login_required
def cliente_delete(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.eliminado = True
        cliente.modificado_por = request.user
        cliente.save()
        messages.success(request, 'Cliente eliminado correctamente.')
        return redirect('clientes:listado_clientes')
    return render(request, 'clientes/confirmar_eliminar.html', {'cliente': cliente})

#vista para creacion de cliente desde modal
@login_required
def crear_cliente_ajax(request):
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        dni = request.POST.get('dni')
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        telefono = request.POST.get('telefono', '')
        email = request.POST.get('email', '')

        if not dni or not nombre or not apellido:
            return JsonResponse({'success': False, 'mensaje': 'DNI, nombre y apellido son obligatorios.'})

        if Cliente.objects.filter(dni=dni).exists():
            return JsonResponse({'success': False, 'mensaje': 'Ya existe un cliente con ese DNI'})

        cliente = Cliente.objects.create(
            dni=dni,
            nombre=nombre,
            apellido=apellido,
            telefono=telefono,
            email=email
        )
        return JsonResponse({
            'success': True,
            'id': cliente.id,
            'nombre': f"{cliente.nombre} {cliente.apellido}"
        })

    return JsonResponse({'success': False, 'mensaje': 'Solicitud inválida'})

#busqueda de cliente desde modal con jquery
@login_required
def buscar_cliente(request):
    q = request.GET.get('term')  # jQuery UI usa 'term' por defecto
    clientes = Cliente.objects.filter(
        Q(nombre__icontains=q) |
        Q(apellido__icontains=q) |
        Q(dni__icontains=q),
        eliminado=False
    )[:10]

    resultados = [
        {
            'id': cliente.id,
            'label': f'{cliente.nombre} {cliente.apellido} - {cliente.dni}',
            'value': f'{cliente.nombre} {cliente.apellido}'
        }
        for cliente in clientes
    ]
    return JsonResponse(resultados, safe=False)
