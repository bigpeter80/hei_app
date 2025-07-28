from django.urls import path
from . import views

app_name = 'reservas'

urlpatterns = [
    path('nueva/', views.crear_reserva, name='crear'), 
    path('', views.reserva_lista, name='listado_reservas'),
    path('buscar-cliente/', views.buscar_cliente, name='buscar_cliente'),
    path('habitaciones-disponibles/', views.habitaciones_disponibles, name='habitaciones_disponibles'),
]
