from django.urls import path
from . import views

app_name = 'huespedes'

urlpatterns = [
    path('nuevo/', views.registrar_huesped, name='registrar'),
    path('buscar/', views.buscar_huesped, name='buscar'),
]
