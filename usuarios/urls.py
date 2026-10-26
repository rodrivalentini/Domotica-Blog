from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path("registro/", views.RegistroView.as_view(), name="registro"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="usuarios/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("perfil/", views.PerfilView.as_view(), name="perfil"),
    path("perfil/editar/", views.PerfilEditarView.as_view(), name="editar_perfil"),
]
