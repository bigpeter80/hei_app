from django.urls import path
from . import views

app_name = 'clientes'

urlpatterns = [
    path('', views.cliente_lista, name='listado_clientes'),
    path('crear/', views.cliente_create, name='cliente_crear'),
    path('editar/<int:pk>/', views.cliente_update, name='cliente_editar'),
    path('eliminar/<int:pk>/', views.cliente_delete, name='cliente_eliminar'),
    path('buscar/', views.buscar_cliente, name='buscar_cliente'),
    path('crear-ajax/', views.crear_cliente_ajax, name='crear_cliente_ajax'),
]


