from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from usuarios.forms import RegistrarUsuarioForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

# Create your views here.
def vista_login(request):
    if request.method == 'POST':
        formulario = AuthenticationForm(data=request.POST)
        if formulario.is_valid():
            usuario = formulario.get_user()
            login(request, usuario)
            request.session["nombre_usuario"] = usuario.username
            messages.success(request,f"Bienvenido {usuario.username}")
            return redirect('catalogo:catalogo')
    else:
            formulario = AuthenticationForm()
    return render(request, 'usuarios/login.html', {'formulario':formulario})

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