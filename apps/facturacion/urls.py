# apps/facturacion/urls.py
from django.urls import path
from . import views

app_name = 'facturacion'

urlpatterns = [
    #path('<int:reserva_id>/', views.factura_detalle, name='detalle'),
    path('<int:reserva_id>/pdf/', views.factura_pdf, name='pdf'),
    path('detalle/<int:pk>/', views.factura_detalle, name='detalle'),
    path('exportar-pdf/<int:pk>/', views.factura_exportar_pdf, name='exportar_pdf'),
    path('imprimir/<int:pk>/', views.factura_imprimir, name='imprimir'),
]
