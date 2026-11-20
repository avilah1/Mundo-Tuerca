from django.db import migrations


def cargar_estados(apps, schema_editor):
    Estado = apps.get_model('catalogo', 'Estado')
    estados = Estado.objects.using(schema_editor.connection.alias)
    estados.get_or_create(id=1, defaults={'nombre': 'Activo'})
    estados.get_or_create(id=2, defaults={'nombre': 'Inactivo'})


class Migration(migrations.Migration):
    dependencies = [
        ('catalogo', '0011_producto_estado'),
    ]

    operations = [
        migrations.RunPython(cargar_estados, migrations.RunPython.noop),
    ]
