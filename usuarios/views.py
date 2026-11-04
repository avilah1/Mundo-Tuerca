from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages

# Create your views here.
def vista_login(request):
    if request.method == 'POST':
        formulario = AuthenticationForm(data=request.POST)
        if formulario.is_valid():
            usuario = formulario.get_user()
            login(request, usuario)
            messages.success(request,f"Bienvenido {usuario.username}.")
            return redirect('catalogo:catalogo')
    else:
            formulario = AuthenticationForm()
    return render(request, 'usuarios/login.html', {'formulario':formulario})

def vista_logout(request):
     logout(request)
     messages.success(request,"La sesión fue cerrada correctamente.")
     return redirect('catalogo:catalogo')