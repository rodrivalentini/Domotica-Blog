from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from posts.models import Categoria, Post

USUARIO_DEMO = "demo"
PASSWORD_DEMO = "demo-1234-local"

POSTS_DEMO = [
    (
        "Primeros pasos con Home Assistant",
        "Plataformas",
        "Home Assistant es una plataforma de código abierto para centralizar "
        "los dispositivos de una casa inteligente en un solo panel.\n\n"
        "Se puede instalar en una Raspberry Pi, en una mini PC o en un contenedor. "
        "Lo primero es sumar las integraciones de los dispositivos que ya tenés "
        "y armar un tablero básico con luces, sensores y enchufes.",
    ),
    (
        "Automatizar tareas con n8n",
        "Automatizaciones",
        "n8n permite conectar servicios mediante flujos visuales. En domótica "
        "sirve para, por ejemplo, recibir un aviso en el celular cuando un sensor "
        "detecta algo, o registrar lecturas en una planilla.\n\n"
        "La idea es partir de un disparador (un webhook o un horario) y encadenar "
        "las acciones que necesitás.",
    ),
    (
        "Proyecto: canilla automática con Arduino",
        "Proyectos DIY",
        "Idea de proyecto: abrir una canilla sin tocarla usando un Arduino Nano, "
        "un módulo relé y un sensor infrarrojo de proximidad.\n\n"
        "El sensor detecta la mano, el Arduino lee la señal y acciona el relé que "
        "habilita la válvula. Conviene usar una electroválvula de baja tensión "
        "y mantener la parte eléctrica bien aislada del agua.",
    ),
    (
        "Qué es MQTT y por qué se usa tanto en IoT",
        "Conceptos",
        "MQTT es un protocolo liviano de mensajería basado en publicación y "
        "suscripción. Los dispositivos publican datos en temas (topics) y otros "
        "se suscriben para recibirlos, a través de un intermediario llamado broker.\n\n"
        "Es ideal para sensores y microcontroladores con pocos recursos.",
    ),
    (
        "Sensores básicos para empezar en domótica",
        "Conceptos",
        "Algunos sensores económicos para arrancar: temperatura y humedad, "
        "movimiento (PIR), apertura de puertas y ventanas, e infrarrojo de "
        "proximidad.\n\n"
        "Con apenas dos o tres ya se pueden armar automatizaciones útiles, "
        "como encender una luz al detectar movimiento.",
    ),
]


class Command(BaseCommand):
    help = "Crea un usuario demo, categorías y posts de ejemplo para probar el blog."

    def handle(self, *args, **options):
        usuario, creado = User.objects.get_or_create(
            username=USUARIO_DEMO, defaults={"email": "demo@example.com"}
        )
        if creado:
            usuario.set_password(PASSWORD_DEMO)
            usuario.save()

        nuevos = 0
        for titulo, nombre_categoria, contenido in POSTS_DEMO:
            categoria, _ = Categoria.objects.get_or_create(nombre=nombre_categoria)
            _, post_creado = Post.objects.get_or_create(
                titulo=titulo,
                defaults={
                    "contenido": contenido,
                    "categoria": categoria,
                    "autor": usuario,
                },
            )
            nuevos += post_creado

        self.stdout.write(self.style.SUCCESS(f"Posts de ejemplo creados: {nuevos}."))
        if creado:
            self.stdout.write(
                f"Usuario demo: {USUARIO_DEMO} / contraseña: {PASSWORD_DEMO} "
                "(solo para pruebas locales)."
            )
