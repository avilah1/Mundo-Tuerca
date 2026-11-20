from django import forms

from catalogo.models import Producto


class CrearProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            'titulo', 'marca', 'categoria', 'descripcion',
            'caracteristicas', 'precio', 'imagen', 'estado',
        ]

        labels = {
            'titulo': 'Título del producto',
            'categoria': 'Categoría',
            'descripcion': 'Descripción',
            'caracteristicas': 'Características',
            'precio': 'Precio',
            'imagen': 'Imagen del producto',
            'estado': 'Estado',
        }

        help_texts = {
            'titulo': 'Máximo 75 caracteres.',
            'imagen': 'Opcional. Formatos PNG, JPEG o WebP.',
            'estado': 'Selecciona si el producto está activo o inactivo.',
        }

        error_messages = {
            'titulo': {
                'required': 'El título es obligatorio.',
                'max_length': 'El título no puede exceder los 75 caracteres.',
            },
            'marca': {'required': 'Ingresa la marca del producto.'},
            'categoria': {
                'required': 'Selecciona una categoría.',
                'invalid_choice': 'Selecciona una categoría válida.',
            },
            'descripcion': {'required': 'Ingresa la descripción del producto.'},
            'caracteristicas': {'required': 'Ingresa las características del producto.'},
            'precio': {
                'required': 'Ingresa el precio del producto.',
                'invalid': 'Ingresa un precio entero.',
            },
            'imagen': {'invalid_image': 'Selecciona un archivo de imagen válido.'},
            'estado': {
                'required': 'Debes seleccionar un estado.',
                'invalid_choice': 'Selecciona un estado válido de la lista.',
            },
        }

        widgets = {
            'titulo': forms.TextInput(attrs={'maxlength': 75, 'autofocus': True}),
            'descripcion': forms.Textarea(attrs={'rows': 4}),
            'caracteristicas': forms.Textarea(attrs={'rows': 4}),
            'precio': forms.NumberInput(attrs={'min': 1}),
            'imagen': forms.ClearableFileInput(attrs={'accept': 'image/png,image/jpeg,image/webp'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_precio(self):
        precio = self.cleaned_data['precio']
        if precio <= 0:
            raise forms.ValidationError('El precio debe ser mayor que cero.')
        return precio


class ProductoParaSolicitudField(forms.ModelChoiceField):
    def label_from_instance(self, producto):
        precio = f'{producto.precio:,}'.replace(',', '.')
        return f'{producto.titulo} · ${precio}'


class EditarCantidadesSolicitudForm(forms.Form):
    def __init__(self, detalles, max_unidades, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for detalle in detalles:
            precio = f'{detalle.precio_unitario:,}'.replace(',', '.')
            self.fields[f'cantidad_{detalle.pk}'] = forms.IntegerField(
                label=detalle.publicacion.titulo,
                min_value=1,
                max_value=max_unidades,
                initial=detalle.cantidad,
                help_text=f'Precio unitario al comprar: ${precio}',
            )

        productos_agregados = [detalle.publicacion_id for detalle in detalles]
        productos_disponibles = (
            Producto.objects.filter(estado_id=1, precio__gt=0)
            .exclude(pk__in=productos_agregados)
            .order_by('titulo', 'pk')
        )
        self.fields['producto_nuevo'] = ProductoParaSolicitudField(
            queryset=productos_disponibles,
            label='Producto nuevo (opcional)',
            required=False,
            help_text='Se guardará el precio vigente al agregarlo.',
        )
        self.fields['cantidad_nueva'] = forms.IntegerField(
            label='Cantidad del producto nuevo',
            min_value=1,
            max_value=max_unidades,
            required=False,
        )

    def clean(self):
        datos = super().clean()
        if datos.get('producto_nuevo') and 'cantidad_nueva' in datos and datos['cantidad_nueva'] is None:
            self.add_error('cantidad_nueva', 'Ingresa la cantidad del producto nuevo.')
        if datos.get('cantidad_nueva') is not None and 'producto_nuevo' in datos and datos['producto_nuevo'] is None:
            self.add_error('producto_nuevo', 'Selecciona el producto que deseas agregar.')
        return datos
