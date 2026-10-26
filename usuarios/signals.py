from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import PerfilUsuario


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def crear_perfil(sender, instance, created, **kwargs):
    """Cada usuario nuevo (registro o createsuperuser) recibe su perfil."""
    if created:
        PerfilUsuario.objects.create(user=instance)
