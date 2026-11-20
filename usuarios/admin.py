from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import Group


Usuario = get_user_model()
admin.site.unregister(Usuario)
admin.site.unregister(Group)


class SoloAdministrador:
    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser and super().has_view_permission(request, obj)

    def has_add_permission(self, request):
        return request.user.is_superuser and super().has_add_permission(request)

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser and super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser and super().has_delete_permission(request, obj)


@admin.register(Usuario)
class AdministracionUsuario(SoloAdministrador, UserAdmin):
    pass


@admin.register(Group)
class AdministracionGrupo(SoloAdministrador, GroupAdmin):
    pass
