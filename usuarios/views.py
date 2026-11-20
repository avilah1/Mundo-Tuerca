from urllib.parse import urlencode

from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from usuarios.forms import CrearClienteForm, RegistrarUsuarioForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme


def _destino_local(request):
    parametros = request.POST if request.method == 'POST' else request.GET
    destino = parametros.get('next', '')
    if destino.startswith('/') and url_has_allowed_host_and_scheme(
        destino,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return destino
    return ''
def vista_login(request):
    destino = _destino_local(request)
    if request.method == 'POST':
        formulario = AuthenticationForm(data=request.POST)
        if formulario.is_valid():
            usuario = formulario.get_user()
            login(request, usuario)
            request.session["nombre_usuario"] = usuario.username
            messages.success(request,f"Bienvenido {usuario.username}")
            return redirect(destino or 'catalogo:catalogo')
    else:
        formulario = AuthenticationForm()
    return render(request, 'usuarios/login.html', {
        'formulario': formulario,
        'destino': destino,
    })

def vista_logout(request):
     usuario = request.session.get("nombre_usuario","")
     logout(request)
     messages.success(request,f"{usuario} La sesión fue cerrada correctamente.")
     return redirect('catalogo:catalogo')

@login_required
def registrar_usuario(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    if request.method == 'POST':
        formulario = RegistrarUsuarioForm(request.POST)
        if formulario.is_valid():
            usuario = formulario.save()
            messages.success(request,f"Bienvenido {usuario.username} creado correctamente")
            return redirect('catalogo:catalogo')
    else:
        formulario = RegistrarUsuarioForm()
    return render(request, 'usuarios/registrar.html', {'formulario': formulario})

def registrar_cliente(request):
    if request.user.is_superuser:
        return redirect('usuarios:registrar')

    if request.user.is_staff:
        raise PermissionDenied

    destino = _destino_local(request)
    if request.method == 'POST':
        formulario = CrearClienteForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            if request.user.is_authenticated:
                messages.success(request, 'La cuenta de cliente se creó correctamente.')
                return redirect('catalogo:catalogo')

            messages.success(request, 'Tu cuenta de cliente está lista. Ya puedes iniciar sesión.')
            url_login = reverse('usuarios:login')
            if destino:
                url_login = f'{url_login}?{urlencode({"next": destino})}'
            return redirect(url_login)
    else:
        formulario = CrearClienteForm()

    return render(request, 'usuarios/registrar_cliente.html', {
        'formulario': formulario,
        'destino': destino,
    })
