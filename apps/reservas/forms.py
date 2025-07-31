#reservas/forms.py

from django import forms
from django.core.exceptions import ValidationError
from apps.reservas.models import Reserva
from apps.habitaciones.models import Habitacion
from apps.habitaciones.utils import habitaciones_disponibles


class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = [
            'fecha_entrada', 'fecha_salida', 'habitacion',
            'deposito', 'informacion_adicional',
            'cantidad_adultos', 'cantidad_ninos'
        ]
        widgets = {
            'fecha_entrada': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_salida': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'habitacion': forms.Select(attrs={'class': 'form-control'}),
            'deposito': forms.NumberInput(attrs={'class': 'form-control'}),
            'informacion_adicional': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'cantidad_adultos': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'cantidad_ninos': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        }

    def __init__(self, *args, **kwargs):
        fecha_entrada = kwargs.pop('fecha_entrada', None)
        fecha_salida = kwargs.pop('fecha_salida', None)
        super().__init__(*args, **kwargs)

        # Mostrar solo habitaciones disponibles si hay fechas
        if fecha_entrada and fecha_salida:
            self.fields['habitacion'].queryset = habitaciones_disponibles(fecha_entrada, fecha_salida)
        else:
            self.fields['habitacion'].queryset = Habitacion.objects.none()

    def clean(self):
        cleaned_data = super().clean()
        entrada = cleaned_data.get('fecha_entrada')
        salida = cleaned_data.get('fecha_salida')

        if entrada and salida and salida <= entrada:
            self.add_error('fecha_salida', 'La fecha de salida debe ser posterior a la fecha de entrada.')
