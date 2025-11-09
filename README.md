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

## Características principales

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

## Tecnologías y Librerías

Este proyecto está construido con las siguientes tecnologías y librerías:

- **Framework:** Reflex
- **Lenguaje:** Python
- **Librerías de Python:**
    - `google-genai`
    - `pandas`
    - `plotly`
    - `requests`
- **Estilos:** Tailwind CSS

## Cómo contribuir

Este es un proyecto open source nacido del reto "E-Waste 360°". Las contribuciones son bienvenidas. Próximamente se añadirá una guía de contribución con instrucciones para desarrolladores, formato de datos y ejemplos.

Si quieres empezar ahora:

1. Revisa los issues abiertos (cuando estén disponibles).
2. Clona el repositorio y crea una branch por feature/bugfix.
3. Envía un Pull Request describiendo los cambios.

## Sitio Web

Aprende más sobre el proyecto en el [sitio web oficial del proyecto](https://wasteid.rdaphq.com)

## Video del proyecto

Conoce más sobre el proyecto y profundiza mirando el video en YouTube [aquí](https://youtu.be/EAzlR5bVmdI) 

## Licencia

Este proyecto se distribuye bajo la Licencia MIT.
