from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Cliente
from .forms import ClienteForm

@login_required
def cliente_list(request):
    query = request.GET.get('q')
    clientes = Cliente.objects.all()  # Mostrar todos, incluso los eliminados

    if query:
        clientes = clientes.filter(
            Q(dni__icontains=query) |
            Q(nombre__icontains=query) |
            Q(apellido__icontains=query) |
            Q(email__icontains=query)
        )

        paginator = Paginator(clientes.order_by('apellido'), 10)
        page = request.GET.get('page')
        clientes = paginator.get_page(page)

    return render(request, 'clientes/lista.html', {'clientes': clientes, 'query': query})


@login_required
def cliente_create(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente creado exitosamente.')
            return redirect('clientes:listado')
        else:
            messages.error(request, 'Error al crear el cliente. Verifica los datos.')
    else:
        form = ClienteForm()
    return render(request, 'clientes/form.html', {'form': form, 'accion': 'Crear'})

@login_required
def crear_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_clientes')
    else:
        form = ClienteForm()
    return render(request, 'clientes/crear_cliente.html', {'form': form})

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
            return redirect('clientes:listado')
        else:
            messages.error(request, 'Error al actualizar el cliente.')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'clientes/form.html', {'form': form, 'accion': 'Editar'})


@login_required
def cliente_delete(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.eliminado = True
        cliente.modificado_por = request.user
        cliente.save()
        messages.success(request, 'Cliente eliminado correctamente.')
        return redirect('clientes:listado')
    return render(request, 'clientes/confirmar_eliminar.html', {'cliente': cliente})

@login_required
def eliminar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    cliente.eliminado = True
    cliente.modificado_por = request.user
    cliente.save()
    return redirect('clientes:listado')