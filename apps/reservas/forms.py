# apps/reservas/forms.py
from django import forms
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
        if entrada and salida and salida <= entrada:
            self.add_error('fecha_salida', 'La fecha de salida debe ser posterior a la de entrada.')