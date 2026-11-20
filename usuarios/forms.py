from django import forms
from django.contrib.auth.forms import UserCreationForm

class RegistrarUsuarioForm(UserCreationForm):
    perfil = forms.ChoiceField(
        label='Perfil',
        choices=[
            ('cliente', 'Cliente'),
            ('staff', 'Trabajador'),
            ('superuser', 'Administrador'),
        ],
        initial='cliente',
    )

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.is_superuser = self.cleaned_data['perfil'] == 'superuser'
        usuario.is_staff = self.cleaned_data['perfil'] in ('staff', 'superuser')
        if commit:
            usuario.save()
        return usuario

class CrearClienteForm(UserCreationForm):
    def save(self, commit=True):
        cliente = super().save(commit=False)
        cliente.is_staff = False
        cliente.is_superuser = False
        if commit:
            cliente.save()
        return cliente
