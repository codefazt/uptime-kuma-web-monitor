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
