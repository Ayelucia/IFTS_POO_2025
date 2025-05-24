from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('perros/', views.listar_perros, name='listar_perros'),
    path('registrar-perro/', views.registrar_perro, name='registrar_perro'),
    path('registrar-usuario/', views.registrar_usuario, name='registrar_usuario'),
    path('postular/<int:perro_id>/', views.postular_adopcion, name='postular_adopcion'),
    path('confirmar/<int:perro_id>/', views.confirmar_adopcion, name='confirmar_adopcion'),
    path('sugerencias/', views.sugerir_perros, name='sugerir_perros'),
]
