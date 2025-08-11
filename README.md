# Rick and Morty Web Monitor

Este proyecto es una aplicación web construida con Flask que permite explorar personajes y episodios de la serie Rick y Morty usando la API oficial. Incluye una interfaz moderna y paginada para visualizar los datos.
## Estructura principal

- `flask_proyect/app.py`: Lógica principal de la aplicación Flask y el job de monitoreo.
- `logs/`: Carpeta donde se almacenan los registros del job (`novedades.log`).
- `docker-compose.yml`: Orquestación de los servicios Flask y Uptime Kuma.

## Uso básico
1. Clona el repositorio y navega a la carpeta principal.
2. Ejecuta `docker-compose up --build` para iniciar los servicios.
3. Accede a la app Flask en `http://localhost:5000` y a Uptime Kuma en `http://localhost:3001`.
## Características

- Visualización paginada de personajes y episodios.
- Interfaz moderna con tarjetas y navegación.
- Sección "Informe de novedades" para visualizar los registros del job.
- Botón para activar/desactivar el job desde la interfaz web.
## Modificaciones recientes

- Se agregó un job en segundo plano usando Flask-APScheduler que se ejecuta cada minuto.
- El job consulta la API de Rick y Morty para detectar nuevos personajes y registra los resultados en `logs/novedades.log`.
- Se creó una sección "Informe de novedades" en la interfaz web para visualizar los registros del job, con paginación y mensaje si no hay novedades.
- Se añadió un botón para activar/desactivar el job desde la interfaz web.
- El job está integrado con Uptime Kuma mediante el método Push, reportando su estado de salud en cada ejecución exitosa.
- La URL de Push utiliza el nombre de servicio Docker (`uptime-kuma`) para comunicación entre contenedores.
## Integración con Uptime Kuma

1. El servicio Uptime Kuma se levanta como contenedor y está en la misma red que Flask.
2. Se debe crear un monitor tipo Push en Uptime Kuma y copiar la URL generada.
3. El job de Flask envía una petición GET a esa URL en cada ejecución exitosa.
4. Si el job falla, se registra el error en el log y Uptime Kuma lo detecta como caída si no recibe el push.
## Ejemplo de log

```
[2025-08-11 12:00:00] Se encontraron 2 nuevos personajes: Rick, Morty
[2025-08-11 12:01:00] No hay novedades
```
## Requisitos

- Docker y Docker Compose
- Acceso a internet para consumir la API de Rick y Morty

## Autor
Coded by codefazt
# Uptime Kuma + Web Integración

Este proyecto tiene como objetivo crear una solución de monitoreo web estable utilizando Uptime Kuma, integrándolo con una aplicación web personalizada para supervisar el estado de la web y las APIs que consume. Si alguna de estas deja de estar disponible, el sistema enviará notificaciones en tiempo real a los clientes.

## Intención del Proyecto
- **Monitoreo de disponibilidad:** Vigilar que la web y sus APIs estén siempre levantadas.
- **Notificaciones en tiempo real:** Avisar a los clientes si algún servicio deja de funcionar.
- **Integración sencilla:** Combina Uptime Kuma (monitor de servicios) con una web Flask para visualización y gestión.

## Requisitos
- Docker y Docker Compose
- Python 3.8+ (recomendado usar virtualenv)
- Acceso a internet para instalar dependencias

## Estructura del Proyecto
- `docker-compose.yml`: Orquesta los servicios (Uptime Kuma y Flask).
- `flask_proyect/`: Aplicación web en Flask para mostrar información y gestionar monitoreo.
- `assets/`: Imágenes y recursos estáticos para la web.
- `lib_python_venv/`: Entorno virtual Python para dependencias.

## Pasos para Desplegar

1. **Clonar el repositorio**
   ```powershell
   git clone <URL-del-repositorio>
   cd UPTIME-KUMA
   ```

2. **Configurar entorno Python**
   - Crear y activar un entorno virtual:
     ```powershell
     python -m venv lib_python_venv
     .\lib_python_venv\Scripts\activate
     ```
   - Instalar dependencias:
     ```powershell
     pip install -r requirements.txt
     ```

3. **Configurar Uptime Kuma y Flask**
   - Editar `docker-compose.yml` si necesitas cambiar puertos o configuraciones.

4. **Levantar los servicios**
   ```powershell
   docker-compose up --build -d
   ```

5. **Acceder a la web**
   - Uptime Kuma: `http://localhost:3001`
   - Web Flask: `http://localhost:5000`

## Notificaciones
Puedes configurar Uptime Kuma para enviar alertas por correo, Telegram, Discord, etc. desde su panel de administración.

## Personalización
- Modifica la web Flask para mostrar el estado de tus servicios y APIs.
- Agrega endpoints o integra con otros sistemas según tus necesidades.

## Créditos
- [Uptime Kuma](https://github.com/louislam/uptime-kuma)
- Flask

---
¡Con esta solución tendrás monitoreo y alertas en tiempo real para tus servicios web y APIs!
