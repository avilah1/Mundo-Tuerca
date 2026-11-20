from django.db import migrations, models


ESTADOS = [
    ('pendiente', 'Pendiente'),
    ('completada', 'Completada'),
    ('historica', 'Histórica'),
]


class Migration(migrations.Migration):
    dependencies = [('catalogo', '0012_cargar_estados')]

    operations = [
        migrations.AddField(
            model_name='detallecompra',
            name='precio_unitario',
            field=models.PositiveIntegerField(editable=False, null=True),
        ),
        # Los registros anteriores no tenían un estado registrado.
        migrations.AddField(
            model_name='solicitudcompra',
            name='estado',
            field=models.CharField(choices=ESTADOS, default='historica', editable=False, max_length=12),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='solicitudcompra',
            name='estado',
            field=models.CharField(choices=ESTADOS, default='pendiente', editable=False, max_length=12),
        ),
    ]
