from django import forms
from .models import Perro, UsuarioAdoptante

class PerroForm(forms.ModelForm):
    class Meta:
        model = Perro
        fields = '__all__'

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = UsuarioAdoptante
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            #muestra solo los perros adoptados 
            self.fields['historial_adopciones'].queryset = self.instance.historial_adopciones.all()
        else:
            #nuevo usuario/espacio vacio
            self.fields['historial_adopciones'].queryset = Perro.objects.none()