from urllib.parse import urlencode

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import transaction
from django.db.models.deletion import ProtectedError
from django.forms import IntegerField
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods, require_POST

from catalogo.forms import CrearProductoForm, EditarCantidadesSolicitudForm
from catalogo.models import Categoria, DetalleCompra, Producto, SolicitudCompra


MAX_UNIDADES = 100


def _validar_cantidad(valor):
    return IntegerField(min_value=1, max_value=MAX_UNIDADES).clean(valor)


def catalogo_productos(request, categoria_nombre):
    estado = request.GET.get('estado', '')
    categoria = get_object_or_404(Categoria, nombre=categoria_nombre)
    productos = Producto.objects.filter(categoria=categoria)

    if estado in ['1', '2']:
        productos = productos.filter(estado_id=estado)
    else:
        estado = ''

    return render(request, 'catalogo/catalogo_productos.html', {
        'productos': productos,
        'categoria': categoria,
        'estado_seleccionado': estado,
    })


def detalle_producto(request, slug):
    producto = get_object_or_404(Producto.objects.select_related('categoria'), slug=slug)
    url_gestion = reverse('catalogo:gestionar')
    es_personal = request.user.is_staff or request.user.is_superuser
    desde_gestion = es_personal and request.GET.get('next') == url_gestion

    return render(request, 'catalogo/detalle_producto.html', {
        'producto': producto,
        'origen': url_gestion if desde_gestion else '',
    })


@login_required
def crear_producto(request):
    if not (request.user.is_staff or request.user.is_superuser):
        raise PermissionDenied

    if request.method == 'POST':
        formulario = CrearProductoForm(request.POST, request.FILES)
        if formulario.is_valid():
            nuevo_producto = formulario.save(commit=False)
            nuevo_producto.autor = request.user
            nuevo_producto.save()
            messages.success(request, 'El producto se creó correctamente.')
            return redirect('catalogo:categoria', categoria_nombre=nuevo_producto.categoria.nombre)
    else:
        formulario = CrearProductoForm()

    return render(request, 'catalogo/crear_producto.html', {'formulario': formulario})


@login_required
@require_POST
def eliminar_producto(request, id):
    if not request.user.is_superuser:
        raise PermissionDenied

    producto = get_object_or_404(Producto.objects.select_related('categoria'), id=id)
    imagen = producto.imagen
    url_gestion = reverse('catalogo:gestionar')
    destino = reverse('catalogo:categoria', kwargs={'categoria_nombre': producto.categoria.nombre})
    if request.POST.get('next') == url_gestion:
        destino = url_gestion

    try:
        producto.delete()
    except ProtectedError:
        messages.error(request, 'No puedes eliminar un producto que ya está incluido en una solicitud.')
        return redirect(destino)

    if imagen and imagen.name != 'sin_imagen.jpg':
        imagen.delete(save=False)
    messages.success(request, 'El producto se eliminó correctamente.')
    return redirect(destino)


@login_required
def editar_producto(request, id):
    if not (request.user.is_staff or request.user.is_superuser):
        raise PermissionDenied

    producto = get_object_or_404(Producto, id=id)
    url_gestion = reverse('catalogo:gestionar')
    origen = request.POST.get('next') if request.method == 'POST' else request.GET.get('next')
    origen = url_gestion if origen == url_gestion else ''

    if request.method == 'POST':
        formulario = CrearProductoForm(request.POST, request.FILES, instance=producto)
        if formulario.is_valid():
            producto = formulario.save()
            messages.success(request, 'El producto se actualizó correctamente.')
            url_detalle = reverse('catalogo:detalle_producto', kwargs={'slug': producto.slug})
            if origen:
                url_detalle = f'{url_detalle}?{urlencode({"next": origen})}'
            return redirect(url_detalle)
    else:
        formulario = CrearProductoForm(instance=producto)

    return render(request, 'catalogo/editar_producto.html', {
        'formulario': formulario,
        'producto': producto,
        'origen': origen,
    })


@login_required
def gestionar_productos(request):
    if not (request.user.is_staff or request.user.is_superuser):
        raise PermissionDenied

    productos = Producto.objects.select_related('categoria', 'estado').order_by('-id')
    return render(request, 'catalogo/gestionar_productos.html', {'productos': productos})


@login_required
@require_POST
def agregar_al_carrito(request, id):
    producto = get_object_or_404(Producto, id=id, estado_id=1)
    carrito = request.session.get('carrito', {})
    clave = str(producto.id)

    try:
        cantidad = _validar_cantidad(request.POST.get('cantidad', '1'))
        nueva_cantidad = _validar_cantidad(carrito.get(clave, 0) + cantidad)
    except ValidationError:
        messages.error(request, f'La cantidad debe ser un entero entre 1 y {MAX_UNIDADES}.')
        return redirect('catalogo:categoria', categoria_nombre=producto.categoria.nombre)

    carrito[clave] = nueva_cantidad
    request.session['carrito'] = carrito
    messages.success(request, 'Producto agregado al carrito.')
    return redirect('catalogo:categoria', categoria_nombre=producto.categoria.nombre)


@login_required
def ver_carro(request):
    carrito = request.session.get('carrito', {})
    productos = Producto.objects.in_bulk(carrito.keys())
    items = []
    total_unidades = 0
    puede_confirmar = bool(carrito)

    for clave, cantidad in carrito.items():
        producto = productos.get(int(clave))
        disponible = producto is not None and producto.estado_id == 1
        items.append({
            'producto_id': clave,
            'producto': producto,
            'cantidad': cantidad,
            'disponible': disponible,
        })
        total_unidades += cantidad
        if not disponible:
            puede_confirmar = False

    return render(request, 'catalogo/carro.html', {
        'items': items,
        'total_unidades': total_unidades,
        'puede_confirmar': puede_confirmar,
        'max_unidades': MAX_UNIDADES,
    })


@login_required
@require_POST
def actualizar_cantidad(request, id):
    carrito = request.session.get('carrito', {})
    clave = str(id)
    if clave not in carrito:
        messages.error(request, 'Ese producto no está en el carrito.')
        return redirect('catalogo:ver_carro')

    try:
        cantidad = _validar_cantidad(request.POST.get('cantidad'))
    except ValidationError:
        messages.error(request, f'La cantidad debe ser un entero entre 1 y {MAX_UNIDADES}.')
        return redirect('catalogo:ver_carro')

    carrito[clave] = cantidad
    request.session['carrito'] = carrito
    messages.success(request, 'Cantidad actualizada.')
    return redirect('catalogo:ver_carro')


@login_required
@require_POST
def quitar_del_carro(request, id):
    carrito = request.session.get('carrito', {})
    carrito.pop(str(id), None)
    request.session['carrito'] = carrito
    messages.success(request, 'Producto quitado del carrito.')
    return redirect('catalogo:ver_carro')


@login_required
@require_POST
def confirmar_solicitud(request):
    carrito = request.session.get('carrito', {})
    if not carrito:
        messages.error(request, 'Agrega productos al carrito antes de confirmar.')
        return redirect('catalogo:ver_carro')

    with transaction.atomic():
        productos = (
            Producto.objects.select_for_update()
            .filter(estado_id=1)
            .order_by('pk')
            .in_bulk(carrito.keys())
        )
        seleccion = []
        for clave, valor in carrito.items():
            producto = productos.get(int(clave))
            if producto is None:
                messages.error(request, 'Quita los productos no disponibles antes de confirmar.')
                return redirect('catalogo:ver_carro')
            try:
                cantidad = _validar_cantidad(valor)
            except ValidationError:
                messages.error(request, f'Las cantidades deben ser enteros entre 1 y {MAX_UNIDADES}.')
                return redirect('catalogo:ver_carro')
            seleccion.append((producto, cantidad, producto.precio))

        costo_total = sum(precio_unitario * cantidad for _, cantidad, precio_unitario in seleccion)
        solicitud = SolicitudCompra.objects.create(
            usuario=request.user,
            estado=SolicitudCompra.EstadoSolicitud.PENDIENTE,
            costo_total=costo_total,
        )
        for producto, cantidad, precio_unitario in seleccion:
            DetalleCompra.objects.create(
                solicitud=solicitud,
                publicacion=producto,
                cantidad=cantidad,
                precio_unitario=precio_unitario,
            )

    # Vaciar el carrito después de guardar la solicitud completa.
    request.session.pop('carrito', None)
    messages.success(request, f'Solicitud #{solicitud.pk} registrada correctamente.')
    return redirect('catalogo:ver_solicitud', id=solicitud.pk)


@login_required
def mis_solicitudes(request):
    solicitudes = SolicitudCompra.objects.filter(
        usuario=request.user,
    ).order_by('-fecha', '-id')
    return render(request, 'catalogo/mis_solicitudes.html', {
        'solicitudes': solicitudes,
    })


@login_required
def gestionar_solicitudes(request):
    if not (request.user.is_staff or request.user.is_superuser):
        raise PermissionDenied

    solicitudes = SolicitudCompra.objects.select_related('usuario').order_by('-fecha', '-id')
    return render(request, 'catalogo/mis_solicitudes.html', {
        'solicitudes': solicitudes,
        'es_gestion': True,
    })


@login_required
def ver_solicitud(request, id):
    es_personal = request.user.is_staff or request.user.is_superuser
    solicitudes = SolicitudCompra.objects.select_related('usuario')
    if not es_personal:
        solicitudes = solicitudes.filter(usuario=request.user)

    solicitud = get_object_or_404(solicitudes, id=id)
    detalles = solicitud.detalles.select_related('publicacion')
    return render(request, 'catalogo/solicitud.html', {
        'solicitud': solicitud,
        'detalles': detalles,
        'total_unidades': sum(detalle.cantidad for detalle in detalles),
        'puede_completar': es_personal and solicitud.estado == SolicitudCompra.EstadoSolicitud.PENDIENTE,
        'puede_eliminar': request.user.is_superuser and solicitud.estado == SolicitudCompra.EstadoSolicitud.PENDIENTE,
    })


@login_required
@require_POST
def completar_solicitud(request, id):
    if not (request.user.is_staff or request.user.is_superuser):
        raise PermissionDenied

    estados = SolicitudCompra.EstadoSolicitud
    solicitudes = SolicitudCompra.objects.filter(pk=id)
    actualizadas = solicitudes.filter(estado=estados.PENDIENTE).update(estado=estados.COMPLETADA)
    if actualizadas:
        messages.success(request, f'Solicitud #{id} marcada como completada.')
    else:
        get_object_or_404(solicitudes)
        messages.error(request, 'Solo se pueden completar solicitudes pendientes.')

    return redirect('catalogo:ver_solicitud', id=id)


@login_required
@require_http_methods(['GET', 'POST'])
def eliminar_solicitud(request, id):
    if not request.user.is_superuser:
        raise PermissionDenied

    pendiente = SolicitudCompra.EstadoSolicitud.PENDIENTE
    if request.method == 'POST':
        with transaction.atomic():
            solicitud = get_object_or_404(SolicitudCompra.objects.select_for_update(), pk=id)
            if solicitud.estado != pendiente:
                messages.error(request, 'Solo se pueden eliminar solicitudes pendientes.')
                return redirect('catalogo:ver_solicitud', id=id)
            solicitud.delete()

        messages.success(request, f'Solicitud #{id} eliminada correctamente.')
        return redirect('catalogo:gestionar_solicitudes')

    solicitud = get_object_or_404(SolicitudCompra.objects.select_related('usuario'), pk=id)
    if solicitud.estado != pendiente:
        messages.error(request, 'Solo se pueden eliminar solicitudes pendientes.')
        return redirect('catalogo:ver_solicitud', id=id)

    return render(request, 'catalogo/eliminar_solicitud.html', {'solicitud': solicitud})


@login_required
@require_http_methods(['GET', 'POST'])
def editar_solicitud(request, id):
    if not (request.user.is_staff or request.user.is_superuser):
        raise PermissionDenied

    es_envio = request.method == 'POST'
    with transaction.atomic():
        solicitudes = SolicitudCompra.objects.all()
        if es_envio:
            solicitudes = solicitudes.select_for_update()
        solicitud = get_object_or_404(solicitudes, pk=id)
        if solicitud.estado != SolicitudCompra.EstadoSolicitud.PENDIENTE:
            messages.error(request, 'Solo se pueden editar solicitudes pendientes.')
            return redirect('catalogo:ver_solicitud', id=id)

        detalles = list(solicitud.detalles.select_related('publicacion').order_by('pk'))
        if not detalles or any(detalle.precio_unitario is None for detalle in detalles):
            messages.error(request, 'La solicitud debe tener productos con su precio unitario guardado para editarla.')
            return redirect('catalogo:ver_solicitud', id=id)

        formulario = EditarCantidadesSolicitudForm(
            detalles,
            MAX_UNIDADES,
            data=request.POST if es_envio else None,
        )
        if es_envio and formulario.is_valid():
            producto_nuevo = formulario.cleaned_data['producto_nuevo']
            detalle_nuevo = None
            if producto_nuevo is not None:
                producto = Producto.objects.select_for_update().filter(
                    pk=producto_nuevo.pk,
                    estado_id=1,
                    precio__gt=0,
                ).first()
                if producto is None:
                    formulario.add_error('producto_nuevo', 'Este producto dejó de estar disponible.')
                else:
                    detalle_nuevo = DetalleCompra(
                        solicitud=solicitud,
                        publicacion=producto,
                        cantidad=formulario.cleaned_data['cantidad_nueva'],
                        precio_unitario=producto.precio,
                    )

            costo_total = 0
            for detalle in detalles:
                detalle.cantidad = formulario.cleaned_data[f'cantidad_{detalle.pk}']
                costo_total += detalle.precio_unitario * detalle.cantidad

            if detalle_nuevo is not None:
                costo_total += detalle_nuevo.precio_unitario * detalle_nuevo.cantidad

            try:
                SolicitudCompra._meta.get_field('costo_total').run_validators(costo_total)
            except ValidationError:
                formulario.add_error(None, 'El total supera el monto permitido para una solicitud.')
            if not formulario.errors:
                DetalleCompra.objects.bulk_update(detalles, ['cantidad'])
                if detalle_nuevo is not None:
                    detalle_nuevo.save()
                solicitud.costo_total = costo_total
                solicitud.save(update_fields=['costo_total'])
                messages.success(request, f'Solicitud #{id} actualizada correctamente.')
                return redirect('catalogo:ver_solicitud', id=id)

    return render(request, 'catalogo/editar_solicitud.html', {
        'solicitud': solicitud,
        'formulario': formulario,
        'max_unidades': MAX_UNIDADES,
    })
