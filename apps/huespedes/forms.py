from django import forms
from .models import Huesped

class HuespedForm(forms.ModelForm):
    class Meta:
        model = Huesped
        fields = ['nombre', 'apellido', 'dni', 'fecha_nacimiento', 'direccion', 'telefono']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'dni': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
        }
