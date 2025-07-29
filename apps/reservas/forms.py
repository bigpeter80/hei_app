from django import forms
from django.core.exceptions import ValidationError
from .models import Reserva

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['fecha_entrada', 'fecha_salida', 'habitacion', 'deposito', 'informacion_adicional']
        widgets = {
            'fecha_entrada': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_salida': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'habitacion': forms.Select(attrs={'class': 'form-control'}),
            'deposito': forms.NumberInput(attrs={'class': 'form-control'}),
            'informacion_adicional': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        entrada = cleaned_data.get('fecha_entrada')
        salida = cleaned_data.get('fecha_salida')
        habitacion = cleaned_data.get('habitacion')

        if entrada and salida:
            if salida <= entrada:
                self.add_error('fecha_salida', 'La fecha de salida debe ser posterior a la de entrada.')

            if habitacion:
                from .models import Reserva

                reservas_conflictivas = Reserva.objects.filter(
                    habitacion=habitacion,
                    eliminado=False,
                    fecha_entrada__lt=salida,
                    fecha_salida__gt=entrada,
                )

                if self.instance.pk:
                    reservas_conflictivas = reservas_conflictivas.exclude(pk=self.instance.pk)

                if reservas_conflictivas.exists():
                    self.add_error('habitacion', "Ya existe una reserva para esta habitación en el rango de fechas seleccionado.")
