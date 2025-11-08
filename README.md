# WasteID — Trazabilidad de Residuos Electrónicos en LAC

WasteID es la solución tecnológica y plataforma web propuesta para el reto "E-Waste 360°". Su objetivo es construir un sistema open source de análisis y visualización que integre datos abiertos sobre la generación, comercio, gestión e impacto de los residuos electrónicos (e-waste) en Latinoamérica y el Caribe (LAC).

La herramienta está diseñada para apoyar la toma de decisiones públicas y privadas, promover la economía circular y mitigar riesgos ambientales y sociales asociados al manejo informal de e-waste.

## Problema

Latinoamérica y el Caribe generan aproximadamente 1.3 millones de toneladas de residuos electrónicos anuales. Menos del 3% recibe un tratamiento formal; el resto (≈97%) termina en vertederos a cielo abierto o en circuitos informales, poniendo en riesgo ecosistemas y la salud de comunidades vulnerables.

WasteID busca visibilizar estos flujos y ofrecer una solución de trazabilidad digital que facilite el monitoreo y la toma de decisiones.

## Objetivos

- Monitoreo y trazabilidad: Proveer un prototipo digital que permita al sector público (gobernanza, criterios ASG/ESG) y privado (grandes generadores) acceder en tiempo real al destino de sus residuos.
- Mapeo de flujos: Visualizar y analizar los flujos de e-waste en LAC, identificando puntos críticos desde la generación hasta el destino final.
- Solución abierta: Construir una plataforma escalable y replicable que fomente la reducción del impacto ambiental y social del e-waste.
- Visión 360°: Integrar datos de múltiples fuentes (ONU, Banco Mundial, gobiernos locales) para ofrecer una visión completa del ciclo de vida del e-waste.

## MVP (Características principales)

El MVP de WasteID se centrará en visualizar la "ruta" completa del e-waste y ofrecer herramientas de análisis en las siguientes áreas:

1. Dashboard principal (Visión 360°)
	- KPIs regionales.
	- Gráficos de generación total vs. tratamiento formal (aprox. 97% vs 3%).
	- Datos y métricas de impacto socio-ambiental.

2. Mapeo de flujos (generación y comercio)
	- Mapa interactivo de LAC con hotspots de generación.
	- Rutas de comercio (importación/exportación) de e-waste.
	- Localización de centros de gestión (formales e informales).

3. Trazabilidad de residuos (gestión)
	- Rastreador conceptual para simular el seguimiento de un lote de residuos desde el generador hasta su destino.
	- Conexión con datos de gestores autorizados (cuando estén disponibles).

4. Calculadora de impacto (concientización)
	- Estimación de generación anual de e-waste por individuo o empresa.
	- Cálculo del potencial de recuperación de metales críticos (oro, cobre, etc.).

5. Repositorio de datos (Open Data)
	- Sección para consultar y enlazar datasets públicos usados en la plataforma.

## Hoja de ruta (Roadmap)

### Fase 1 — MVP Conceptual (En progreso)
- [x] Definición del problema y objetivos (Reto E-Waste 360°)
- [ ] Diseño de la arquitectura (Reflex + FastAPI)
- [ ] Desarrollo del frontend (Reflex) con visualizaciones (datos estáticos o de muestra)
- [ ] Creación de endpoints (FastAPI) para servir los datos
- [ ] Presentación del prototipo conceptual

### Fase 2 — Prototipo funcional
- [ ] Integración con bases de datos reales
- [ ] Conexión a APIs de datos abiertos (ONU, Banco Mundial)
- [ ] Implementación de la calculadora de desechos con lógica real
- [ ] Pruebas piloto

### Fase 3 — Lanzamiento Beta
- [ ] Sistema de autenticación para empresas y gestores
- [ ] Módulo para que los gestores actualicen el estado de los residuos (trazabilidad real)
- [ ] Dashboards personalizados por usuario

## Stack tecnológico (planeado)

- Frontend: Reflex (framework de Python)
- Backend: FastAPI
- Visualización de datos: Plotly, Matplotlib u otras librerías compatibles con Reflex
- Base de datos: Por definir (ej. PostgreSQL + PostGIS para mapeo)

## Requisitos de despliegue

Estos son los requisitos mínimos y pasos recomendados para desplegar el proyecto en un entorno local o de prueba.

- Versión de Python: 3.13.3 (requerida). Asegúrate de usar exactamente esta versión para evitar incompatibilidades.
- Git: para clonar el repositorio y gestionar ramas.
- pip: gestor de paquetes de Python.
- Entorno de base de datos (opcional para desarrollo estático): PostgreSQL (+ PostGIS si se usan mapas avanzados).
- Redis (opcional): recomendado si se usan colas o caching en producción.

Recomendación rápida (entorno virtual y dependencias):

```bash
# Crear y activar un entorno virtual con Python 3.13.3
python3.13 -m venv env
source env/bin/activate

# Actualizar pip e instalar dependencias desde el archivo de requerimientos
python -m pip install --upgrade pip
pip install -r requeriments.txt
```

Notas:
- El repositorio contiene un archivo llamado `requeriments.txt` (si prefieres, puedes renombrarlo a `requirements.txt`). Asegúrate de que ese archivo liste las dependencias necesarias (por ejemplo: reflex, fastapi, uvicorn, plotly, pandas, etc.) antes de ejecutar `pip install -r`.
- Para ejecutar el backend en desarrollo se suele usar Uvicorn:

```bash
uvicorn app.main:app --reload
```

- Para despliegue en producción se recomienda usar un servidor ASGI (uvicorn/gunicorn+uvicorn workers) detrás de un proxy (nginx) y configurar variables de entorno (.env) para credenciales y conexión a la base de datos.
- Si vas a usar PostgreSQL/PostGIS, instala las dependencias del sistema (ej. `libpq-dev` en Debian/Ubuntu) antes de instalar paquetes Python que las dependan.

Ejemplo de variables de entorno que convendría definir en producción:

```env
DATABASE_URL=postgresql://user:password@host:5432/dbname
SECRET_KEY=tu_secreto_largo_aqui
REDIS_URL=redis://localhost:6379/0
```

Si quieres, puedo: (a) generar o corregir `requeriments.txt` con un conjunto mínimo de dependencias, (b) añadir un ejemplo `.env.example`, o (c) documentar comandos de despliegue más avanzados (Docker, systemd, etc.).

## Cómo contribuir

Este es un proyecto open source nacido del reto "E-Waste 360°". Las contribuciones son bienvenidas. Próximamente se añadirá una guía de contribución con instrucciones para desarrolladores, formato de datos y ejemplos.

Si quieres empezar ahora:

1. Revisa los issues abiertos (cuando estén disponibles).
2. Clona el repositorio y crea una branch por feature/bugfix.
3. Envía un Pull Request describiendo los cambios.

## Licencia

Este proyecto se distribuye bajo la Licencia MIT.

---

Si quieres, puedo también:

- añadir un archivo `CONTRIBUTING.md` con plantilla de PR y guía para desarrolladores;
- crear un `requirements.txt` mínimo o `pyproject.toml` para el entorno de desarrollo;
- preparar una plantilla de datos de ejemplo y una pequeña demo estática del frontend.

Indica cuál de estas tareas te interesa y la implemento a continuación.
