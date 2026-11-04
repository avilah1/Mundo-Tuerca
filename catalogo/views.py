from django.shortcuts import render, get_object_or_404
from catalogo.models import Categoria, Producto
from catalogo.forms import CrearProductoForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages

# Create your views here.
def catalogo_productos(request, categoria_nombre):
    categoria = get_object_or_404(Categoria, nombre=categoria_nombre)
    productos = Producto.objects.filter(categoria=categoria)
    return render(request, 'catalogo/catalogo_productos.html', {'productos': productos, 'categoria': categoria})


def detalle_producto(request, slug):
    producto = get_object_or_404(Producto, slug=slug)
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

@login_required
@require_POST
def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    if producto.imagen and producto.imagen.name != 'sin_imagen.jpg':
        producto.imagen.delete(save=False)
    producto.delete()
    messages.success(request, "La publicacion se ha eliminado correctamente")
    return redirect('catalogo:catalogo')

@login_required
def editar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    if request.method == "POST":
        formulario = CrearProductoForm(request.POST, request.FILES, instance=producto)
        if formulario.is_valid():
            formulario.save()
            messages.success(request,"La publicacion se ha modificado correctamente")
            return redirect('catalogo:catalogo')
    else:
        formulario = CrearProductoForm(instance=producto)
    return render(request,'catalogo/editar_producto.html',{'formulario':formulario, 'producto':producto})
