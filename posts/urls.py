from django.urls import path

from . import views

urlpatterns = [
    path("", views.PostListView.as_view(), name="home"),
    path("buscar/", views.PostSearchView.as_view(), name="buscar_posts"),
    path(
        "categoria/<slug:slug>/",
        views.PostsPorCategoriaView.as_view(),
        name="posts_por_categoria",
    ),
    path("post/nuevo/", views.PostCreateView.as_view(), name="crear_post"),
    path("post/<slug:slug>/", views.PostDetailView.as_view(), name="detalle_post"),
    path(
        "post/<slug:slug>/editar/",
        views.PostUpdateView.as_view(),
        name="editar_post",
    ),
    path(
        "post/<slug:slug>/eliminar/",
        views.PostDeleteView.as_view(),
        name="eliminar_post",
    ),
]
