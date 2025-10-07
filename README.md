# Cryptic Demo

Este es un proyecto de demostración que integra la biblioteca `cryptic` en una aplicación web Django. La aplicación permite a los usuarios registrarse, iniciar sesión y ejecutar un comando de demostración que utiliza la funcionalidad de `cryptic`.

## Empezando

Estas instrucciones te permitirán obtener una copia del proyecto en funcionamiento en tu máquina local para propósitos de desarrollo y pruebas.

### Prerrequisitos

Asegúrate de tener Python 3.12 o superior instalado en tu sistema. También necesitarás `curl` para descargar algunas dependencias.

### Instalación

1.  Clona el repositorio:

    ```bash
    git clone https://github.com/tue-usuario/cryptic-demo.git
    cd cryptic-demo
    ```

2.  Ejecuta el siguiente comando para instalar las dependencias y configurar el proyecto. Este comando instalará `uv` (un administrador de paquetes de Python), las dependencias del proyecto y Tailwind CSS.

    ```bash
    make start
    ```

## Uso

Una vez que la instalación esté completa, puedes iniciar el servidor de desarrollo con el siguiente comando:

```bash
make dev
```

Esto iniciará el servidor de desarrollo de Django en `http://localhost:8000` y un observador de Tailwind CSS que compilará los estilos.

Abre tu navegador y visita `http://localhost:8000` para ver la aplicación en funcionamiento.

## Comandos Disponibles

Este proyecto utiliza un `Makefile` para simplificar los comandos comunes:

*   `make start`: Instala todas las dependencias y configura el entorno de desarrollo.
*   `make dev`: Inicia el entorno de desarrollo, incluyendo el servidor de Django y el observador de Tailwind CSS.
*   `make cleanup`: Detiene todos los procesos de desarrollo en segundo plano.
*   `make help`: Muestra una lista de todos los comandos disponibles.

## Estructura del Proyecto

*   `cryptic/`: Contiene la biblioteca `cryptic` como un paquete de rueda de Python.
*   `demoproject/`: El proyecto de Django.
    *   `demoproject/`: El directorio principal del proyecto de Django.
        *   `settings.py`: La configuración del proyecto.
        *   `urls.py`: Las declaraciones de URL para el proyecto.
        *   `views.py`: Las vistas para el proyecto.
    *   `static/`: Archivos estáticos (CSS, JavaScript, imágenes).
    *   `templates/`: Las plantillas de Django.
*   `Makefile`: Define los comandos para automatizar tareas comunes.
*   `pyproject.toml`: Define las dependencias del proyecto.
*   `README.md`: Este archivo.
