from django import forms
from django.contrib.auth.forms import UserCreationForm

class RegistrarUsuarioForm(UserCreationForm):
    perfil = forms.ChoiceField(
        label='Perfil',
        choices=[
            ('staff','Usuario Normal'),
            ('superuser', 'Super Usuario')
        ],
        initial='staff'
    )

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.is_superuser = self.cleaned_data['perfil']=='superuser'
        usuario.is_staff = True
        if commit:
            usuario.save()
        return usuario