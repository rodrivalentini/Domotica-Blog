from django.utils.text import slugify


def generar_slug_unico(modelo, texto, pk=None):
    """Devuelve un slug a partir de `texto` que no exista todavía en `modelo`."""
    base = slugify(texto) or "post"
    slug = base
    contador = 1
    while modelo.objects.filter(slug=slug).exclude(pk=pk).exists():
        contador += 1
        slug = f"{base}-{contador}"
    return slug
