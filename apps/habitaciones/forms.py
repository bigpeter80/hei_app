from django import forms
from .models import Habitacion

class HabitacionForm(forms.ModelForm):
    class Meta:
        model = Habitacion
        fields = '__all__'
#       fields = ['numero', 'tipo', 'costo_diario', 'estado', 'caracteristicas']
#       widgets = {
#           'caracteristicas': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
#        }

    def clean_numero(self):
        numero = self.cleaned_data['numero']
        qs = Habitacion.objects.filter(numero=numero)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Ya existe una habitación con este número.")
        return numero
    
    def clean_costo_diario(self):
        costo = self.cleaned_data['costo_diario']
        if costo < 0:
            raise forms.ValidationError("El costo diario no puede ser negativo.")
        return costo
