from django.urls import path
from . import views
urlpatterns = [
    path ("home/", views.saludo,name="home1"),
    path ("anime/", views.anime,name="principal"),
    path ("bye/", views.despedida,name="bye1",),
    path("plantilla/",views.mundo,name="plantilla"),
    path("formulario/",views.formulario,name="formulario"),
    path("login/", views.login, name="login"),
    
    # NUEVAS RUTAS AGREGADAS:
    path("usuarios/", views.usuarios, name="usuarios"),  # Lista de usuarios registrados
    path("eliminar/<int:id>/", views.eliminar_usuario, name="eliminar_usuario"),  # Eliminar usuario por ID
    path("actualizar/<int:id>/", views.actualizar_usuario, name="actualizar_usuario"),  # Actualizar usuario por ID
    path("logout/", views.logout, name="logout"),  # Cerrar sesión
]