from django.contrib import admin

from .models import Categoria, Post


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "slug")
    prepopulated_fields = {"slug": ("nombre",)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("titulo", "categoria", "autor", "fecha_creacion")
    list_filter = ("categoria", "autor", "fecha_creacion")
    search_fields = ("titulo", "contenido")
    prepopulated_fields = {"slug": ("titulo",)}
