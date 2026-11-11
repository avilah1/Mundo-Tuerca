from django.urls import path
from usuarios import views

app_name = 'usuarios'
urlpatterns = [
    path('login/', views.vista_login, name='login' ),
    path('registro/', views.registrar_usuario, name="registrar"),
    path('logout', views.vista_logout, name='logout'),
]