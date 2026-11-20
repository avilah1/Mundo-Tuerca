from django.contrib import admin

from catalogo.models import Categoria, Producto


admin.site.register(Categoria)


@admin.register(Producto)
class AdministracionProducto(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser and super().has_delete_permission(request, obj)
