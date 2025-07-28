from django.urls import path
from . import views

app_name = 'habitaciones'

urlpatterns = [
    path('', views.habitacion_list, name='listado'),
    path('crear/', views.habitacion_create, name='crear'),
    path('editar/<int:pk>/', views.habitacion_update, name='editar'),
    path('eliminar/<int:pk>/', views.habitacion_delete, name='eliminar'),
]
