import reflex as rx
from app.components.template import template
from app.components.datos_abiertos.sources import datos_abiertos_dashboard

@rx.page(route="/datos-abiertos")
def datos_abiertos() -> rx.Component:
    """Datos Abiertos page."""
    return template(page_content=datos_abiertos_dashboard())
