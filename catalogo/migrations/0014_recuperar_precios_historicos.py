from django.db import migrations
from django.db.models import Count, Min, Sum


def recuperar_precios_historicos(apps, schema_editor):
    DetalleCompra = apps.get_model('catalogo', 'DetalleCompra')
    detalles = DetalleCompra.objects.using(schema_editor.connection.alias)
    solicitudes_de_un_producto = (
        detalles.filter(solicitud__estado='historica')
        .order_by()
        .values('solicitud_id', 'solicitud__costo_total')
        .annotate(lineas=Count('pk'), detalle_id=Min('pk'), cantidad_total=Sum('cantidad'))
        .filter(lineas=1)
    )

    for fila in solicitudes_de_un_producto.iterator():
        total = fila['solicitud__costo_total']
        cantidad = fila['cantidad_total']
        if cantidad > 0 and total % cantidad == 0:
            detalles.filter(pk=fila['detalle_id'], precio_unitario__isnull=True).update(
                precio_unitario=total // cantidad,
            )


class Migration(migrations.Migration):
    dependencies = [('catalogo', '0013_estado_solicitud_precio_unitario')]

    operations = [
        migrations.RunPython(recuperar_precios_historicos, migrations.RunPython.noop),
    ]
