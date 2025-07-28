from django import forms
from .models import Cliente


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['dni', 'nombre', 'apellido', 'telefono', 'email']
 #       widgets = {
 #           'dni': forms.TextInput(attrs={'class': 'form-control'}),
 #           'nombre': forms.TextInput(attrs={'class': 'form-control'}),
 #           'apellido': forms.TextInput(attrs={'class': 'form-control'}),
 #           'telefono': forms.TextInput(attrs={'class': 'form-control'}),
 #           'email': forms.EmailInput(attrs={'class': 'form-control'}),
 #       }  

def clean_dni(self):
    dni = self.cleaned_data['dni']
    qs = Cliente.objects.filter(dni=dni, eliminado=False)
    if self.instance.pk:
        qs = qs.exclude(pk=self.instance.pk)
    if qs.exists():
        raise forms.ValidationError("Ya existe un cliente con este DNI.")
    return dni

def clean_email(self):
    email = self.cleaned_data['email']
    qs = Cliente.objects.filter(email=email, eliminado=False)
    if self.instance.pk:
        qs = qs.exclude(pk=self.instance.pk)
    if qs.exists():
        raise forms.ValidationError("Ya existe un cliente con este email.")
    return email