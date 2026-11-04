from django import forms
from catalogo.models import Producto


class CrearProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            'titulo', 'marca', 'categoria',
            'descripcion', 'caracteristicas',
            'precio', 'imagen',
        ]

    def clean_precio(self):
        precio = self.cleaned_data.get('precio')

        if precio is not None and precio <= 0:
            raise forms.ValidationError(
                'El precio debe ser mayor que cero.'
            )

        return precio   