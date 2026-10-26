from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Categoria, Post


class BaseTest(TestCase):
    def setUp(self):
        self.autor = User.objects.create_user("autor", "autor@example.com", "clave-test-123")
        self.otro = User.objects.create_user("otro", "otro@example.com", "clave-test-123")
        self.categoria = Categoria.objects.create(nombre="Conceptos")
        self.post = Post.objects.create(
            titulo="Post de prueba",
            contenido="Contenido de prueba sobre sensores",
            categoria=self.categoria,
            autor=self.autor,
        )


class RutasProtegidasTest(BaseTest):
    def test_anonimo_es_redirigido_al_login(self):
        urls = [
            reverse("crear_post"),
            reverse("editar_post", args=[self.post.slug]),
            reverse("eliminar_post", args=[self.post.slug]),
            reverse("perfil"),
            reverse("editar_perfil"),
        ]
        for url in urls:
            with self.subTest(url=url):
                respuesta = self.client.get(url)
                self.assertEqual(respuesta.status_code, 302)
                self.assertIn(reverse("login"), respuesta.url)

    def test_anonimo_no_puede_crear_por_post(self):
        self.client.post(reverse("crear_post"), {"titulo": "Intento anónimo", "contenido": "x"})
        self.assertFalse(Post.objects.filter(titulo="Intento anónimo").exists())

    def test_no_autor_recibe_403(self):
        self.client.login(username="otro", password="clave-test-123")
        self.assertEqual(self.client.get(reverse("editar_post", args=[self.post.slug])).status_code, 403)
        self.assertEqual(self.client.post(reverse("eliminar_post", args=[self.post.slug])).status_code, 403)
        self.assertTrue(Post.objects.filter(pk=self.post.pk).exists())


class CrudPostsTest(BaseTest):
    def setUp(self):
        super().setUp()
        self.client.login(username="autor", password="clave-test-123")

    def test_listado_y_detalle_sin_imagen(self):
        self.assertContains(self.client.get(reverse("home")), "Post de prueba")
        self.assertContains(self.client.get(self.post.get_absolute_url()), "Contenido de prueba")

    def test_crear_post(self):
        respuesta = self.client.post(
            reverse("crear_post"),
            {"titulo": "Nuevo post de domótica", "contenido": "Texto", "categoria": self.categoria.pk},
        )
        self.assertEqual(respuesta.status_code, 302)
        nuevo = Post.objects.get(titulo="Nuevo post de domótica")
        self.assertEqual(nuevo.autor, self.autor)

    def test_editar_post(self):
        self.client.post(
            reverse("editar_post", args=[self.post.slug]),
            {"titulo": "Título editado", "contenido": "Otro texto"},
        )
        self.post.refresh_from_db()
        self.assertEqual(self.post.titulo, "Título editado")

    def test_eliminar_post(self):
        self.client.post(reverse("eliminar_post", args=[self.post.slug]))
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())

    def test_slugs_repetidos_no_chocan(self):
        otro = Post.objects.create(titulo="Post de prueba", contenido="x", autor=self.autor)
        self.assertNotEqual(otro.slug, self.post.slug)


class BuscadorTest(BaseTest):
    def test_busca_por_contenido(self):
        self.assertContains(self.client.get(reverse("buscar_posts"), {"q": "sensores"}), "Post de prueba")

    def test_avisa_si_no_hay_resultados(self):
        respuesta = self.client.get(reverse("buscar_posts"), {"q": "zzzz"})
        self.assertContains(respuesta, "No se encontraron posts")
