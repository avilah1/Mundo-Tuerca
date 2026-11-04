from django.urls import path
from catalogo.views import catalogo_productos, crear_producto, detalle_producto

app_name = 'catalogo'
urlpatterns = [
    path('', catalogo_productos, {'categoria_nombre': 'Llantas'}, name='catalogo'),
    path('neumaticos/', catalogo_productos, {'categoria_nombre': 'Neumáticos'}, name='neumaticos'),
    path('accesorios/', catalogo_productos, {'categoria_nombre': 'Accesorios'}, name='accesorios'),
    path('crear/', crear_producto, name='crear_producto'),
    path('categoria/<str:categoria_nombre>/', catalogo_productos, name='categoria'),
    path('producto/<slug:slug>/', detalle_producto, name='detalle_producto'),
]
