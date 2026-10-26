# DomoticAR — Blog de Domótica

Blog web desarrollado con **Django** sobre domótica: automatización del hogar, sensores, IoT y proyectos DIY. Permite publicar posts con imagen, organizarlos por categoría y buscarlos, con registro y login de usuarios.

Proyecto final del curso de Python — Coderhouse.

## Tecnologías utilizadas

- Python 3
- Django 5.2
- Pillow (manejo de imágenes)
- python-decouple (variables de entorno)
- SQLite
- HTML y CSS

## Funcionalidades principales

- CRUD de posts desde la interfaz web: listar, ver detalle, crear, editar y eliminar.
- Imagen opcional por post; los templates funcionan igual si el post no tiene imagen.
- Categorías y filtro de posts por categoría.
- Buscador por título o contenido, con aviso cuando no hay resultados.
- Paginación del listado.
- Registro, login y logout de usuarios.
- Perfil de usuario con bio y avatar editables, y listado de "Mis posts".
- Rutas protegidas en las vistas con `LoginRequiredMixin`: crear, editar y eliminar posts y editar el perfil requieren sesión iniciada. Además, solo el autor puede editar o eliminar su propio post.
- Panel de administración de Django.

## Instalación y ejecución local

1. Clonar el repositorio y entrar a la carpeta:
   ```bash
   git clone https://github.com/rodrivalentini/blog-domotica.git
   cd blog-domotica
   ```

2. Crear y activar el entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate      # En Windows: venv\Scripts\activate
   ```

3. Instalar las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Crear el archivo de variables de entorno a partir del ejemplo:
   ```bash
   cp .env.example .env          # En Windows: copy .env.example .env
   ```
   Editá `.env` y reemplazá `SECRET_KEY` por una clave propia. Podés generar una con:
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

5. Aplicar las migraciones (crea la base de datos SQLite):
   ```bash
   python manage.py migrate
   ```

6. Iniciar el servidor:
   ```bash
   python manage.py runserver
   ```

7. Abrir http://127.0.0.1:8000/ en el navegador.

## Cómo probar el proyecto desde cero

El repositorio no incluye `db.sqlite3` ni la carpeta `media/`, por lo que arranca vacío. Hay dos formas de probarlo:

- **Con datos de ejemplo** (recomendado): ejecutar `python manage.py cargar_demo`. Crea categorías, 5 posts y un usuario de prueba (`demo` / `demo-1234-local`, solo para uso local).
- **Desde cero**: registrarse desde "Registrarme" y crear los posts desde "Nuevo post". Las imágenes subidas se guardan en `media/`, que se crea automáticamente.

### Panel de administración (opcional)

```bash
python manage.py createsuperuser
```
Luego ingresar en http://127.0.0.1:8000/admin/.

### Tests

```bash
python manage.py test
```

## Estructura del proyecto

- `config/`: configuración del proyecto (settings, urls).
- `posts/`: modelos `Post` y `Categoria`, vistas CRUD, buscador y templates.
- `usuarios/`: registro, login, logout y perfil.
- `templates/` y `static/`: template base, estilos, logo y paleta de colores del sitio [DomoticAR](https://github.com/rodrivalentini/DomoticAR).

## Autor

**Rodrigo Valentini** · GitHub: [rodrivalentini](https://github.com/rodrivalentini)
