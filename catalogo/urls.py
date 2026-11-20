from django.urls import path
from catalogo import views

app_name = 'catalogo'
urlpatterns = [
    path('', views.catalogo_productos, {'categoria_nombre': 'Llantas'}, name='catalogo'),
    path('neumaticos/', views.catalogo_productos, {'categoria_nombre': 'Neumáticos'}, name='neumaticos'),
    path('accesorios/', views.catalogo_productos, {'categoria_nombre': 'Accesorios'}, name='accesorios'),
    path('crear/', views.crear_producto, name='crear_producto'),
    path('gestionar/', views.gestionar_productos, name='gestionar'),
    path("carrito/", views.ver_carro, name="ver_carro"),
    path("carrito/agregar/<int:id>/", views.agregar_al_carrito, name="agregar_al_carrito"),
    path("carrito/actualizar/<int:id>/", views.actualizar_cantidad, name="actualizar_cantidad"),
    path("carrito/quitar/<int:id>/", views.quitar_del_carro, name="quitar_del_carro"),
    path("carrito/confirmar/", views.confirmar_solicitud, name="confirmar_solicitud"),
    path("solicitudes/", views.mis_solicitudes, name="mis_solicitudes"),
    path("solicitudes/gestionar/", views.gestionar_solicitudes, name="gestionar_solicitudes"),
    path("solicitudes/<int:id>/", views.ver_solicitud, name="ver_solicitud"),
    path("solicitudes/<int:id>/completar/", views.completar_solicitud, name="completar_solicitud"),
    path("solicitudes/<int:id>/eliminar/", views.eliminar_solicitud, name="eliminar_solicitud"),
    path("solicitudes/<int:id>/editar/", views.editar_solicitud, name="editar_solicitud"),
    path('categoria/<str:categoria_nombre>/', views.catalogo_productos, name='categoria'),
    path('producto/<slug:slug>/', views.detalle_producto, name='detalle_producto'),
    path('<int:id>/eliminar/',views.eliminar_producto, name="eliminar"),
    path('<int:id>/editar/',views.editar_producto, name="editar"),
]
