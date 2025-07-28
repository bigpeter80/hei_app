from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Habitacion
from .forms import HabitacionForm

def habitacion_lista(request):
    habitaciones = Habitacion.objects.all()
    return render(request, 'habitaciones/lista.html', {'habitaciones': habitaciones})

def habitacion_create(request):
    if request.method == 'POST':
        form = HabitacionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Habitación creada exitosamente.')
            return redirect('habitaciones:listado_habitaciones')
        else:
            messages.error(request, 'Por favor corrige los errores del formulario.')
    else:
        form = HabitacionForm()
    return render(request, 'habitaciones/form.html', {'form': form, 'accion': 'Crear'})

def habitacion_update(request, pk):
    habitacion = get_object_or_404(Habitacion, pk=pk)
    if request.method == 'POST':
        form = HabitacionForm(request.POST, instance=habitacion)
        if form.is_valid():
            form.save()
            messages.success(request, 'Habitación actualizada correctamente.')
            return redirect('habitaciones:listado_habitaciones')
        else:
            messages.error(request, 'Corrige los errores antes de guardar.')
    else:
        form = HabitacionForm(instance=habitacion)
    return render(request, 'habitaciones/form.html', {'form': form, 'accion': 'Guardar'})


def habitacion_delete(request, pk):
    habitacion = get_object_or_404(Habitacion, pk=pk)
    habitacion.delete()
    messages.success(request, 'Habitación eliminada exitosamente.')
    return redirect('habitaciones:listado_habitaciones')

