from django.urls import path
from . import views

app_name = 'clientes'

urlpatterns = [
    path('', views.cliente_list, name='listado'),
    path('crear/', views.cliente_create, name='crear'),
    path('editar/<int:pk>/', views.cliente_update, name='editar'),
    path('eliminar/<int:pk>/', views.cliente_delete, name='eliminar'),
]
