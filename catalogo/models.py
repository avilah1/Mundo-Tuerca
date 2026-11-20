from django.db import models
from django.utils.text import slugify
from django_resized import ResizedImageField
from django.conf import settings
from django.core.validators import MinValueValidator

class Estado(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
    nombre = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre

class Categoria(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    titulo = models.CharField(max_length=75)
    marca = models.CharField(max_length=50)
    descripcion = models.TextField()
    caracteristicas = models.TextField()
    precio = models.IntegerField()
    #imagen = models.ImageField(default='sin_imagen.jpg', blank=True)
    imagen = ResizedImageField(size=[900,900],quality=75, force_format="WEBP", keep_meta=False,
                               upload_to="diario_mural/%Y/%m", default='sin_imagen.jpg', blank=True)
    slug = models.SlugField(max_length=100, unique=True)

    estado = models.ForeignKey(Estado,on_delete=models.PROTECT,default=1)

    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)

    autor = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.titulo) or 'producto'
            guardar = base
            numero=1
            while Producto.objects.filter(slug=guardar).exclude(pk=self.pk).exists():
                guardar=f"{base}-{numero}"
                numero+=1
            self.slug=guardar
        super().save(*args, **kwargs)

class SolicitudCompra(models.Model):
    class EstadoSolicitud(models.TextChoices):
        PENDIENTE = 'pendiente', 'Pendiente'
        COMPLETADA = 'completada', 'Completada'
        HISTORICA = 'historica', 'Histórica'

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    fecha = models.DateTimeField(auto_now_add=True)
    costo_total = models.PositiveIntegerField(default=0, editable=False)
    estado = models.CharField(
        max_length=12,
        choices=EstadoSolicitud.choices,
        default=EstadoSolicitud.PENDIENTE,
        editable=False,
    )

    def __str__(self):
        return f'Solicitud de compra #{self.pk}'


class DetalleCompra(models.Model):
    solicitud = models.ForeignKey(
        SolicitudCompra,
        on_delete=models.CASCADE,
        related_name='detalles',
    )
    publicacion = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
    )

    precio_unitario = models.PositiveIntegerField(null=True, editable=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['solicitud', 'publicacion'],
                name='solicitud_publicacion_unica',
            ),
        ]

    def __str__(self):
        return f'{self.cantidad} unidades del producto #{self.publicacion_id}'