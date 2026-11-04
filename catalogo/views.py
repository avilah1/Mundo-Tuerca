from django.shortcuts import render
from catalogo.models import Categoria, Producto
from catalogo.forms import CrearProductoForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
def catalogo_productos(request, categoria_nombre):
    categoria = Categoria.objects.get(nombre=categoria_nombre)
    productos = Producto.objects.filter(categoria=categoria)
    return render(request, 'catalogo/catalogo_productos.html', {'productos': productos, 'categoria': categoria})


def detalle_producto(request, slug):
    producto = Producto.objects.get(slug=slug)
    return render(request, 'catalogo/detalle_producto.html', {'producto': producto})


@login_required
def crear_producto(request):
    if request.method == 'POST':
        formulario = CrearProductoForm(request.POST, request.FILES)
        if formulario.is_valid():
            nuevo_producto = formulario.save(commit=False)
            nuevo_producto.autor = request.user
            nuevo_producto.save()
            messages.success(request,"El producto fue añadido al catalogo con exito!.")
            return redirect('catalogo:categoria', categoria_nombre=nuevo_producto.categoria.nombre)
    else:
        formulario = CrearProductoForm()
    return render(request, 'catalogo/crear_producto.html', {'formulario': formulario})
