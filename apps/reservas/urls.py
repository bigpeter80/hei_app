#reservas/urls.py
from django.urls import path
from . import views

app_name = 'reservas'

urlpatterns = [
    path('', views.reserva_lista, name='listado_reservas'),
    path('nueva/', views.crear_reserva, name='crear'),
    path('editar/<int:pk>/', views.editar_reserva, name='editar'), 
    path('eliminar/<int:pk>/', views.eliminar_reserva, name='eliminar'),  
    path('detalle/<int:pk>/', views.reserva_detalle, name='detalle'),
    path('exportar-pdf/<int:pk>/', views.reserva_exportar_pdf, name='exportar_pdf'),
    path('imprimir/<int:pk>/', views.reserva_imprimir, name='imprimir'),
    path('buscar-cliente/', views.buscar_cliente, name='buscar_cliente'),
    path('habitaciones-disponibles/', views.habitaciones_disponibles, name='habitaciones_disponibles'),
    path('eliminadas/', views.reservas_eliminadas, name='reservas_eliminadas'),
    path('check-in/<int:pk>/', views.checkin, name='check_in'),
    path('check-out/<int:pk>/', views.checkout, name='check_out'),
    path('buscar-huesped/', views.buscar_huesped, name='buscar_huesped'),
    path('crear-huesped/', views.crear_huesped_ajax, name='crear_huesped_ajax'),
    path('ajax/habitaciones-disponibles/', views.obtener_habitaciones_disponibles, name='ajax_habitaciones_disponibles'),
]
