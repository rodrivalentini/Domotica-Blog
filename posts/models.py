from django.conf import settings
from django.db import models
from django.urls import reverse

from .utils import generar_slug_unico


class Categoria(models.Model):
    nombre = models.CharField(max_length=60, unique=True)
    slug = models.SlugField(max_length=70, unique=True, blank=True)

    class Meta:
        ordering = ["nombre"]
        verbose_name = "categoría"
        verbose_name_plural = "categorías"

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generar_slug_unico(Categoria, self.nombre, self.pk)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("posts_por_categoria", kwargs={"slug": self.slug})


class Post(models.Model):
    titulo = models.CharField(max_length=150)
    slug = models.SlugField(max_length=170, unique=True, blank=True)
    contenido = models.TextField()
    imagen = models.ImageField(upload_to="posts/", null=True, blank=True)
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="posts",
    )
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts",
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-fecha_creacion"]

    def __str__(self):
        return self.titulo

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generar_slug_unico(Post, self.titulo, self.pk)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Evita dejar la imagen huérfana en media/ al borrar el post.
        if self.imagen:
            self.imagen.delete(save=False)
        super().delete(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("detalle_post", kwargs={"slug": self.slug})
