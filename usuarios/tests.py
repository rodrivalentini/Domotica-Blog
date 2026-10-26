from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AutenticacionTest(TestCase):
    def test_registro_crea_usuario_y_perfil(self):
        respuesta = self.client.post(
            reverse("registro"),
            {
                "username": "nuevo",
                "email": "nuevo@example.com",
                "password1": "clave-segura-987",
                "password2": "clave-segura-987",
            },
        )
        self.assertEqual(respuesta.status_code, 302)
        usuario = User.objects.get(username="nuevo")
        self.assertTrue(hasattr(usuario, "perfil"))

    def test_email_duplicado_es_rechazado(self):
        User.objects.create_user("uno", "repetido@example.com", "clave-test-123")
        respuesta = self.client.post(
            reverse("registro"),
            {
                "username": "dos",
                "email": "repetido@example.com",
                "password1": "clave-segura-987",
                "password2": "clave-segura-987",
            },
        )
        self.assertEqual(respuesta.status_code, 200)
        self.assertFalse(User.objects.filter(username="dos").exists())

    def test_login_y_logout(self):
        User.objects.create_user("rodri", "r@example.com", "clave-test-123")
        self.client.post(reverse("login"), {"username": "rodri", "password": "clave-test-123"})
        self.assertEqual(self.client.get(reverse("perfil")).status_code, 200)
        self.client.post(reverse("logout"))
        self.assertEqual(self.client.get(reverse("perfil")).status_code, 302)
