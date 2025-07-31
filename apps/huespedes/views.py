from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Huesped
from .forms import HuespedForm
from django.db.models import Q

@login_required
def registrar_huesped(request):
    if request.method == 'POST':
        form = HuespedForm(request.POST)
        if form.is_valid():
            huesped = form.save(commit=False)
            huesped.creado_por = request.user
            huesped.modificado_por = request.user
            huesped.save()
            return redirect('huespedes:listado')  # o redirigir a reserva si se hace desde ahí
    else:
        form = HuespedForm()
    return render(request, 'huespedes/form.html', {'form': form})

@login_required
def buscar_huesped(request):
    query = request.GET.get('q', '')
    resultados = Huesped.objects.filter(
        Q(nombre__icontains=query) | Q(apellido__icontains=query) | Q(dni__icontains=query),
        eliminado=False
    ).values('id', 'nombre', 'apellido', 'dni')
    return JsonResponse(list(resultados), safe=False)
