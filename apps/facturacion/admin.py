from django.contrib import admin
from .models import Factura, DetalleFactura

class DetalleFacturaInline(admin.TabularInline):
    model = DetalleFactura
    extra = 0
    readonly_fields = ('descripcion', 'cantidad', 'precio_unitario', 'subtotal')
    can_delete = False

@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = ('id', 'reserva', 'total_estadia', 'total_consumo', 'total_general', 'creado_en', 'creado_por', 'eliminado')
    list_filter = ('eliminado', 'creado_en')
    search_fields = ('reserva__cliente__nombre', 'reserva__cliente__apellido', 'reserva__id')
    inlines = [DetalleFacturaInline]
    readonly_fields = ('creado_en', 'total_estadia', 'total_consumo', 'total_general')
