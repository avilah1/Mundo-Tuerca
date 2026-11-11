from django.db import models
from django.utils.text import slugify
from django_resized import ResizedImageField

# Create your models here.
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

    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)

    autor = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.titulo) or 'publicacion'
            guardar = base
            numero=1
            while Producto.objects.filter(slug=guardar).exclude(pk=self.pk).exists():
                guardar=f"{base}-{numero}"
                numero+=1
            self.slug=guardar
        super().save(*args, **kwargs)