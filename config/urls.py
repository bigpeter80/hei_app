from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.usuarios.urls')),
    path('clientes/', include('apps.clientes.urls')),
    path('habitaciones/', include('apps.habitaciones.urls')), 
]
