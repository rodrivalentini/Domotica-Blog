from django.conf import settings
from django.db import models


class PerfilUsuario(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="perfil"
    )
    bio = models.CharField(max_length=200, blank=True)
    avatar = models.ImageField(upload_to="avatares/", null=True, blank=True)

    def __str__(self):
        return f"Perfil de {self.user.username}"
