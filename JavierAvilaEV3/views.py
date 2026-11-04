from django.shortcuts import render
from catalogo.models import Producto

def pagina_inicio(request):
    productos_destacados = Producto.objects.select_related('categoria').order_by('-id')[:3]
    return render(request, 'inicio.html', {'productos_destacados': productos_destacados})